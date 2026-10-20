from dataclasses import dataclass, field


@dataclass
class Basket[T]:
    items: list[T] = field(default_factory=list)

    def add(self, item: T):
        self.items.append(item)


@dataclass
class Fruit:
    name: str


@dataclass
class Vegetable:
    name: str


banana = Fruit(name="banana")
apple = Fruit(name="apple")
potato = Vegetable(name="potato")
onion = Vegetable(name="onion")

fruits_basket = Basket[Fruit]()
fruits_basket.add(apple)
fruits_basket.add(potato)  # error: potato is not a fruit

vegetable_basket = Basket[Vegetable]()
vegetable_basket.add(onion)
vegetable_basket.add(banana)  # error: banana is not a vegetable

mixed_basket = Basket[Fruit | Vegetable]()
mixed_basket.add(onion)
mixed_basket.add(apple)
