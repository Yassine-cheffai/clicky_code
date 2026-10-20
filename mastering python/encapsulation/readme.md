#### What is Encapsulation?
- Encapsulation is a core principle of object-oriented programming (OOP) that describes the bundling of data (attributes) and the methods (behaviors) that operate on that data into a single unit, typically called a class.

- More importantly, it involves data hiding—restricting direct external access to some of an object's internal components. This ensures that the internal state of an object can only be modified in controlled, predictable ways through a well-defined public interface (methods).


#### What Problems Does It Solve?
- In software development without encapsulation, data is often exposed globally or modified directly from anywhere in the codebase. This leads to several major issues:

    - State Corruption & Invalid Data: Without restrictions, **external code** can assign invalid values to an object's variables (e.g., setting a user's age to `-150` or a bank account balance to a string).

    - Tight Coupling and Fragile Code: If every part of your program relies on the internal implementation of a class, changing how that class stores data requires rewriting code across your entire application.

    - High Cognitive Load: When all internal details are exposed, developers have to understand the entire internal mechanics of a component just to use it, increasing the risk of bugs.

#### What It Is Used For
- Protecting Object Integrity: Ensuring an object always remains in a valid, consistent state.

- Separation of Concerns: Hiding complex implementation details behind simple, clean public methods (abstraction).

- Maintainability: Allowing developers to refactor or completely rewrite internal logic without breaking the rest of the application.

#### Best Practices for Effective Encapsulation
To make the most of encapsulation in your code, follow these standard practices:

- Default to Private: Make all internal attributes (fields/variables) private or protected depending on your programming language, because python does not have the concept of private attributes, use `_` in front the attribute name, example: `_price`. Never expose raw data unless absolutely necessary.

- Expose Controlled Access (Getters and Setters): If external code needs to read or modify internal data, provide specific methods using the `@property` decorator rather than public variables. This allows you to validate inputs before changing state.

- Enforce Invariants: Use setter methods to check constraints. For example:

```python
class Car:
    def __init__(self, max_speed: int) -> None:
        self._max_speed = max_speed

    @property
    def max_speed(self) -> int:
        return self._max_speed

    @max_speed.setter
    def max_speed(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("max speed must be an int")
        if max_speed < 0:
            raise ValueError("max speed must be positive")
        self._max_speed = value
```