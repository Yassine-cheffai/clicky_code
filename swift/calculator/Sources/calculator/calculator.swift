// The Swift Programming Language
// https://docs.swift.org/swift-book

// @main
// struct calculator {
//     static func main() {
//         print("Hello, world!")
//     }
// }


// import Foundation

// /// Performs a basic calculation. Returns nil (after printing an error) if it fails.
// func calculate(_ a: Double, _ op: String, _ b: Double) -> Double? {
//     switch op {
//     case "+":
//         return a + b
//     case "-":
//         return a - b
//     case "*", "x":
//         return a * b
//     case "/":
//         if b == 0 {
//             print("Error: division by zero")
//             return nil
//         }
//         return a / b
//     case "%":
//         if b == 0 {
//             print("Error: modulo by zero")
//             return nil
//         }
//         return fmod(a, b)
//     case "^":
//         return pow(a, b)
//     default:
//         print("Error: unknown operator '\(op)'")
//         return nil
//     }
// }

// /// Prints whole numbers without a trailing ".0" (e.g. 7 instead of 7.0).
// func format(_ value: Double) -> String {
//     if value == value.rounded() && abs(value) < 1e15 {
//         return String(Int(value))
//     }
//     return String(value)
// }

// print("Swift Calculator")
// print("Enter expressions like: 3 + 4   (operators: + - * / % ^)")
// print("Type 'quit' to exit.")

// while true {
//     print("> ", terminator: "")
//     fflush(nil)

//     // readLine() returns nil on end-of-input (Ctrl+D)
//     guard let line = readLine() else { break }

//     let input = line.trimmingCharacters(in: .whitespaces)
//     if input.isEmpty { continue }
//     if ["quit", "exit", "q"].contains(input.lowercased()) { break }

//     let parts = input.split(separator: " ").map(String.init)
//     guard parts.count == 3,
//           let a = Double(parts[0]),
//           let b = Double(parts[2]) else {
//         print("Usage: <number> <operator> <number>   e.g. 12 * 3")
//         continue
//     }

//     if let result = calculate(a, parts[1], b) {
//         print(format(result))
//     }
// }

// print("Goodbye!")

let users = [1: "Alice", 2: "Bob"]

func findUser(id: Int) -> String? {
    return users[id]   // Dictionary lookup already returns an Optional
}

let result = findUser(id: 3)   // type: String?, value: nil


if let name = findUser(id: 1) {
    print("Found \(name)")
} else {
    print("User not found")
}