from dataclasses import dataclass, field

@dataclass(order=True)
class Person:
    _sort_index: int = field(init=False, repr=False)
    first_name: str
    last_name: str
    age: int

    def __post_init__(self):
        self._sort_index = self.age


if __name__ == "__main__":
    tony = Person("tony", "stark", 38)
    hulk = Person("hulk", "the green", 39)
    peter = Person("peter", "parker", 20)
    # Create a list of Person instances
    heroes = [tony, hulk, peter]
    # Print each hero individually
    for hero in heroes:
        print(hero)
    # Print the list representation
    print(heroes)
    # Sort heroes based on age (via _sort_index)
    heroes.sort()
    print(heroes)
