from dataclasses import dataclass, field
import random

HOBBIES = ["football", "tennis", "music", "movies"]


@dataclass(frozen=True, kw_only=True)
class Atom:
    protons: int
    neutrons: int
    electrons: int


@dataclass
class Person:
    first_name: str
    last_name: str
    age: int
    # hobbies: list[str] = field(default_factory=list)
    hobbies: list[str] = field(default_factory=lambda: random.choice(HOBBIES))

    def __lt__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        # This ensures sorting is always dynamic based on current values
        return (self.age, self.first_name, self.last_name) < (other.age, other.first_name, other.last_name)


if __name__ == "__main__":
    tony = Person("tony", "c", 30)
    tony2 = Person("tony", "a", 31)
    tony3 = Person("tony", "b", 29)
    p = [tony, tony2, tony3]
    print(p)
    p.sort()
    print(p)

    carbon = Atom(protons=6, neutrons=6, electrons=6)
    print(carbon)
