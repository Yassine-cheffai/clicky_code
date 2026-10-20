Here's a basic example: a function that looks up a user's name and returns `nil` if the ID doesn't exist.

```swift
let users = [1: "Alice", 2: "Bob"]

func findUser(id: Int) -> String? {
    return users[id]   // Dictionary lookup already returns an Optional
}

let result = findUser(id: 3)   // type: String?, value: nil
```

The return type `String?` tells callers "you might not get a value," and the compiler forces them to deal with that. Below are the common ways to handle it, roughly from most to least recommended.

## 1. `if let` (when you only act on success)

```swift
if let name = findUser(id: 1) {
    print("Found \(name)")
} else {
    print("User not found")
}
```

Inside the braces, `name` is a plain `String`, not an optional.

## 2. `guard let` (early exit, keeps the happy path unindented)

```swift
func greet(id: Int) {
    guard let name = findUser(id: id) else {
        print("Unknown user")
        return
    }
    print("Hello, \(name)")   // name is available for the rest of the function
}
```

Prefer this over nested `if let` when a missing value means the function can't continue.

## 3. Nil-coalescing `??` (when a sensible default exists)

```swift
let name = findUser(id: 3) ?? "Guest"
```

## 4. Optional chaining (when you call something on the result)

```swift
let length = findUser(id: 1)?.count   // Int?, nil if no user
let shout = findUser(id: 1)?.uppercased() ?? "NOBODY"
```

## 5. `map` / `flatMap` (transform without unwrapping manually)

```swift
let greeting = findUser(id: 1).map { "Hello, \($0)!" }   // String?
```

Use `flatMap` when your transform itself returns an optional, to avoid ending up with `String??`.

## 6. `switch` (when you want to be explicit about both cases)

```swift
switch findUser(id: 2) {
case .some(let name): print("Got \(name)")
case .none:           print("Nothing")
}
```

## What to avoid

```swift
let name = findUser(id: 3)!   // crashes at runtime if nil
```

Force unwrapping (`!`) turns a recoverable situation into a crash. Reserve it for cases where nil is truly a programmer error, and even then prefer `guard let` with a clear message, or `preconditionFailure`.

## Best practices summary

- **Use optionals for "absence is normal"**, such as lookups, parsing, or searches. If you need to explain *why* it failed, use `throws` or `Result` instead of returning `nil`.
- **Unwrap as early as possible** with `guard let`, so the rest of your code works with non-optional values.
- **Choose by intent**: `guard let` to bail out, `if let` to branch, `??` for defaults, `?.` for chaining, `map` for transformation.
- **Avoid `!` and implicitly unwrapped optionals (`String!`)** except for things like `@IBOutlet`s that are guaranteed to be set before use.
- **Don't return optional collections**: return an empty array instead of `[String]?`, since empty already means "nothing found."
- **Shadow the name** (`if let name`, or the shorthand `if let name`) rather than inventing names like `unwrappedName`. Swift 5.7+ lets you write `if let name { ... }` when the variable already exists.

And when you need the failure reason, here's the `throws` alternative:

```swift
enum LookupError: Error { case notFound(id: Int) }

func findUserOrThrow(id: Int) throws -> String {
    guard let name = users[id] else { throw LookupError.notFound(id: id) }
    return name
}

do { print(try findUserOrThrow(id: 3)) }
catch { print("Error: \(error)") }
```

Rule of thumb: `nil` means "nothing there," while `throw` means "something went wrong."