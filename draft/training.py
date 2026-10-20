# %%
"""
encapsulation
"""

from unittest import TestCase
from abc import ABC, abstractmethod


class MissingPriceError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Product(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs): ...

    @property
    @abstractmethod
    def price(self) -> int | float: ...

    @price.setter
    @abstractmethod
    def price(self, value: int | float) -> None: ...

    @price.deleter
    @abstractmethod
    def price(self) -> None: ...


class Computer(Product):
    def __init__(self, price: int | float):
        if type(price) not in [int, float]:
            raise TypeError("price must be an int or a float")
        self._price = price

    @property
    def price(self) -> int | float:
        return self._price

    @price.setter
    def price(self, value: int | float):
        if type(value) not in [int, float]:
            raise TypeError("price must be an int or a float")
        if value < 0:
            raise ValueError("Negative price")
        self._price = value

    @price.deleter
    def price(self):
        raise MissingPriceError("a computer must have a price")


# client/external code
try:
    c = Computer(60)
    c.price = 20
    del c.price
except MissingPriceError as e:
    print(e)

c = Computer(60)
c.price = 20
print(c.price)
# test code


class ProductTest(TestCase):
    def test_computer_delete_price(self):
        c = Computer(60)
        with self.assertRaises(MissingPriceError):
            del c.price

    def test_update_computer_price(self):
        c = Computer(60)
        self.assertEqual(c.price, 60)
        c.price = 50
        self.assertEqual(c.price, 50)

    def test_assertion_error_price_not_float_or_int(self):
        """
        Test that the initialisation of the computer with a price of a type other than an int or a float raise an assertion error
        """
        with self.assertRaises(TypeError):
            _ = Computer("200")

        with self.assertRaises(TypeError):
            _ = Computer(True)

    def test_assertion_error_update_price_not_float_or_int(self):
        """
        Test that updating  the computer price with a price of a type other than an int or a float raise an assertion error
        """
        with self.assertRaises(TypeError):
            c = Computer(100)
            c.price = False

        with self.assertRaises(TypeError):
            c = Computer(100)
            c.price = "hello"


ProductTest().test_computer_delete_price()
ProductTest().test_update_computer_price()
ProductTest().test_assertion_error_price_not_float_or_int()
ProductTest().test_assertion_error_update_price_not_float_or_int()
# %%

from abc import ABC, abstractmethod
from unittest import TestCase


class Roue(ABC):
    @abstractmethod
    def roule(self): ...


class RoueA(Roue):
    def roule(self):
        print("je roule en A")


class RoueB(Roue):
    def roule(self):
        print("je roule en B")


class Moteur(ABC):
    @abstractmethod
    def demarrer(self): ...

    @abstractmethod
    def stop(self): ...


class MoteurEssence(Moteur):
    def demarrer(self):
        print("vroom")

    def stop(self):
        print("stopping")

    def __str__(self):
        return "moteur Essence"


class MoteurDiesel(Moteur):
    def demarrer(self):
        print("vroom")

    def stop(self):
        print("stopping")

    def __str__(self):
        return "moteur Diesel"


class Voiture:
    def __init__(self, type_moteur, type_roue):
        self._moteur = type_moteur()
        self._roues = tuple((type_roue() for _ in range(4)))
        self._running = False

    def demarrer(self):
        self._moteur.demarrer()
        for roue in self._roues:
            roue.roule()
        self._running = True

    @property
    def nombre_roue(self):
        return len(self._roues)

    @property
    def moteur(self):
        return self._moteur

    @moteur.setter
    def moteur(self, new_motor: Moteur):
        car_motor_type = type(self._moteur)
        if not isinstance(new_motor, car_motor_type):
            raise TypeError(f"Wrong motor type, this car use a {self._moteur}")
        self._moteur = new_motor

    @moteur.deleter
    def moteur(self):
        if self._running:
            raise Exception("can not remove the moteur while the car is running")

    @property
    def running(self):
        return self._running

    def stop(self):
        self._moteur.stop()
        self._running = False


class Test_Car(TestCase):
    def test_car_is_running(self):
        v = Voiture(type_moteur=MoteurDiesel, type_roue=RoueA)
        v.demarrer()
        self.assertTrue(v.running)

    def test_cannot_remove_motor_car_running(self):
        v = Voiture(type_moteur=MoteurDiesel, type_roue=RoueA)
        v.demarrer()
        with self.assertRaises(Exception):
            del v.moteur

    def test_remove_motor_successfully_car_not_running(self):
        v = Voiture(type_moteur=MoteurDiesel, type_roue=RoueA)
        v.demarrer()
        self.assertTrue(v.running)
        v.stop()
        self.assertFalse(v.running)
        del v.moteur


Test_Car().test_car_is_running()
Test_Car().test_cannot_remove_motor_car_running()
Test_Car().test_remove_motor_successfully_car_not_running()

# %%

from math import pi


class Sphere:
    _attributes = {
        "rayon": lambda rayon: rayon,
        "surface": lambda rayon: 4 * pi * rayon**2,
        "volume": lambda rayon: (4 / 3) * pi * rayon**3,
    }

    def __init__(self, rayon: int | float):
        """
        Create a Sphere
        """
        if type(rayon) not in (int, float):
            raise ValueError("rayon must be an int or a float")
        self.rayon = rayon

    def __getattr__(self, name: str, /):
        if name not in Sphere._attributes:
            raise AttributeError()
        return Sphere._attributes[name](self.rayon)

    def __dir__(self):
        return ("rayon", "surface", "volume")


s = Sphere(rayon=10)
print(f"{s.rayon} m")
print(f"{s.surface} m2")
print(f"{s.volume} m3")
s.rayon = 12
print(f"{s.surface} m2")
print(dir(s))
s.rayon = "hello"


# %%

from datetime import datetime


class ReadOnlyDDN:
    def __init__(self, ddn):
        self.data = {}

    def __get__(self, instance, owner):
        return self.data[instance]

    def __set__(self, instance, value):
        if instance in self.data:
            raise ValueError("can not change")
        self.data[instance] = value


class Personne:
    ddn = ReadOnlyDDN("ddn")

    def __init__(self, nom, ddn):
        self.nom = nom
        self.ddn = ddn


p = Personne(nom="toto", ddn=datetime(2000, 1, 1))
print(p.ddn)
print(p.nom)

p.ddn = None
del p.ddn


# %%


class Personne:
    compteur = 0

    def __init__(self, name):
        self.name = name
        Personne.compteur += 1

    def __del__(self):
        Personne.compteur -= 1


p1 = Personne("toto")
p2 = Personne("titi")
print(Personne.compteur)


# %%
from unittest import TestCase


class Person:
    count = 0

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be an str")
        if name == "":
            raise ValueError("Empty name")
        self._name = name
        Person.count += 1

    def __del__(self):
        print("deleting")
        Person.count -= 1

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        if not isinstance(new_name, str):
            raise TypeError("Name must be a string")

        if new_name == "":
            raise ValueError("Empty name")

        self._name = new_name



yassine = Person("yassine")
yassine.name = ""
id(yassine)

# p1 = Person("tom")
# p2 = Person("jemmy")
# print(Person.count)
# del p2
# print(Person.count)
class TestPerson(TestCase):
    def test_name_is_a_str(self):
        with self.assertRaises(TypeError):
            yassine = Person(4)

    def test_name_update_str(self):
        with self.assertRaises(TypeError):
            yassine = Person("Yassine")
            yassine.name = True

    def test_name_empty_str(self):
        with self.assertRaises(ValueError):
            print(Person.count)
            yassine = Person("")


    def test_update_with_empty_name(self):
        with self.assertRaises(ValueError):
            yassine = Person("Yassine")
            print(Person.count)
            yassine.name = ""


    def test_count_person(self):
        p1 = Person("tom")
        p2 = Person("jemmy")
        self.assertEqual(Person.count, 2)
        del p2
        self.assertEqual(Person.count, 1)


# TestPerson().test_name_is_a_str()
# TestPerson().test_name_update_str()
# TestPerson().test_name_empty_str()
# TestPerson().test_update_with_empty_name()
# TestPerson().test_count_person()
# %%

from math import pi


class Sphere:
    _attributes = {
        "rayon": lambda rayon: rayon,
        "surface": lambda rayon: 4 * pi * rayon**2,
        "volume": lambda rayon: (4 / 3) * pi * rayon**3,
    }

    def __init__(self, rayon: int | float):
        """
        Create a Sphere
        """
        if type(rayon) not in (int, float):
            raise ValueError("rayon must be an int or a float")
        self._rayon = rayon

    @property
    def rayon(self):
        return self._rayon

    @rayon.setter
    def rayon(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("bad value")
        self._rayon = value

    @property
    def surface(self):
        return Sphere._attributes["surface"](self.rayon)

    @property
    def volume(self):
        return Sphere._attributes["volume"](self.rayon)

    def __dir__(self):
        return ("rayon", "surface", "volume")


s = Sphere(rayon=10)
print(f"{s.rayon} m")
print(f"{s.surface} m2")
print(f"{s.volume} m3")
s.rayon = 12
print(f"{s.surface} m2")
print(dir(s))
s.rayon = "hello"


# %%


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


p = Point(x=2, y=3)
p.z = 4  # not permitted cause of __slots__
print(f"{p.x=}")


# %%

from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def bouger(self):
        pass

    @abstractmethod
    def manger(self):
        pass


class Carnivore:
    def manger(self):
        print("je mange de la viande")


class Herbivore:
    def manger(self):
        print("je mange de l'herbe")


class Omnivore:
    def manger(self):
        print("je mange de tout")


class Quadrupede:
    def bouger(self):
        print("je galope")


class Bipede:
    def bouger(self):
        print("je marche")


class Lion(Carnivore, Quadrupede, Animal):
    pass


class Gazelle(Herbivore, Quadrupede, Animal):
    pass


class Singe(Omnivore, Bipede, Animal):
    pass


zoo = (Lion(), Gazelle(), Singe())
for animal in zoo:
    animal.manger()
    animal.bouger()
    print()


# %%

# design pattern: chain of responsability
from enum import Enum


class Statut(Enum):
    CADRE = 0
    NON_CADRE = 1


class Employe:
    def __init__(self, nom, brut, statut):
        self._nom = nom
        self._brut = brut
        self._net = brut
        self._statut = statut

    @property
    def brut(self):
        return self._brut

    @property
    def net(self):
        return self._net

    @property
    def statut(self):
        return self._statut


class EtapeCSG:
    @classmethod
    def process(cls, emp):
        emp._net = emp._brut * 0.925


class EtapeRDS:
    @classmethod
    def process(cls, emp):
        emp._net = emp._net * 0.971


class EtapeAPEC:
    @classmethod
    def process(cls, emp):
        if emp.statut == Statut.CADRE and emp.net > 2500:
            emp._net -= (emp._brut - 2500) * 0.02


class Pipeline(EtapeCSG, EtapeRDS, EtapeAPEC):
    @classmethod
    def process(cls, emp):
        for etape in cls.__bases__:
            etape.process(emp)


emp = Employe(nom="toto", brut=3200, statut=Statut.CADRE)

Pipeline.process(emp)
print(f"{emp.brut} {emp.net}")


# %%
# design pattern composite
from abc import ABC, abstractmethod
from weakref import proxy


class Element(ABC):
    def __init__(self, name, parent):
        if name == "":
            raise ValueError("invalid element name")
        self._name = name
        self._parent = parent

    def __str__(self):
        return self._output(indent_level=0)

    def _output(self, indent_level):
        return (
            f"{'  ' * indent_level}{self.__class__.__name__}: {self.name}"
            + self._on_outputted(indent_level)
        )

    @abstractmethod
    def _on_outputted(self, indent_level):
        pass

    @property
    @abstractmethod
    def size(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def absolute_name(self):
        left_part = self._parent.absolute_name if self._parent else ""
        return f"{left_part}/{self._name}"


class File(Element):
    def __init__(self, name, size, parent):
        super().__init__(name, parent)
        Partition()._check_remaining_size(size)
        self._size = size

    def _on_outputted(self, indent_level):
        return ""

    @property
    def size(self):
        return self._size


class Shortcut(Element):
    def __init__(self, name, target, parent):
        super().__init__(name, parent)
        self._target = target

    def _on_outputted(self, indent_level):
        try:
            s = self._target.absolute_name
        except:
            s = "inexisting element"
        return f" --> {s}"

    @property
    def size(self):
        return 0


class Folder(Element):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self._children = {}

    def __iter__(self):
        return iter(self._children.values())

    @staticmethod
    def _key_from_name(element_name):
        return element_name.upper()

    def _check_name(self, element_name):
        key = Folder._key_from_name(element_name)
        if key in self._children:
            raise Exception(f"{element_name} already exists")
        return key

    def _on_outputted(self, indent_level):
        s = ""
        indent_level += 1
        for element in self._children.values():
            s += "\n" + element._output(indent_level)
        return s

    def create_file(self, file_name, file_size):
        key = self._check_name(file_name)
        file = File(file_name, file_size, parent=self)
        self._children[key] = file
        return proxy(file)

    def create_shortcut(self, shortcut_name, target):
        key = self._check_name(shortcut_name)
        shortcut = Shortcut(shortcut_name, target, parent=self)
        self._children[key] = shortcut
        return proxy(shortcut)

    def create_folder(self, folder_name):
        key = self._check_name(folder_name)
        folder = Folder(folder_name, parent=self)
        self._children[key] = folder
        return proxy(folder)

    def remove_element(self, element_name):
        key = self._key_from_name(element_name)
        if not key in self._children:
            raise Exception(f"{element_name} doesn't exist")
        del self._children[key]

    @property
    def size(self):
        return sum(element.size for element in self._children.values())

    def children(self, type_element=Element):
        for element in self._children.values():
            if isinstance(element, type_element):
                yield element
            if isinstance(element, Folder):
                yield from element.children(type_element)


class Partition(Folder):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_capacity"):
            super().__init__("R1", None)
            self._capacity = 10_000

    def _check_remaining_size(self, desired_size):
        if self.remaining_size < desired_size:
            raise Exception("capacity overflow")

    @property
    def remaining_size(self):
        return self._capacity - self.size


if __name__ == "__main__":
    try:
        r1 = Partition()
        f1 = r1.create_file(file_name="F1", file_size=899)
        r2 = r1.create_folder(folder_name="R2")
        f2 = r2.create_file("F2", 7124)
        r1.create_shortcut(shortcut_name="shortcut on F2", target=f2)
        for element in r1.children(type_element=File):
            print(element.absolute_name)
        print()
        for element in r1.children(type_element=Shortcut):
            print(element.absolute_name)
        print()
        for element in r1.children(type_element=Folder):
            print(element.absolute_name)
        print()
        for element in r1.children(type_element=Element):
            print(element.absolute_name)
        print()
        for element in r1.children():
            print(element.absolute_name)
        print()

        for element in r1:
            print(element.absolute_name)

    except Exception as e:
        print(e)


# %%
def squares(value: int):
    for i in range(value):
        yield (i**2)


# yield from => transorm a list to generator
#
t = (1, 2, 3)


def list_to_generator(t):
    yield from t


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


class Fibonacci:
    def __init__(self, max_terms):
        self.max_terms = max_terms
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == self.max_terms:
            raise StopIteration
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result


gen = fibonacci()
for _ in range(10):
    print(next(gen))

for x in Fibonacci(10):
    print(x)


# %%
# Meta class
# type est un metaclass
# class est un plan de construction d'une object, le meta class est un plan de construction d'un class


class Meta(type):
    def __new__(cls, name, bases, dct):
        print(f"creating class {name}")
        for base in bases:
            print(base.__name__)
        for attribute in dct:
            print(attribute)
        return super().__new__(cls, name, bases, dct)


class A(metaclass=type):
    pass  # default


class B:
    pass


class C:
    pass


class MyClass(A, B, C, metaclass=Meta):
    VALEUR_MIN = 1
    VALEUR_MAX = 100

    def do_it(self):
        print("****")


# %%
# class attribute herited access to/copied by the object , updated, deleted
class Test:
    x = 5


t = Test()
print(t.x)  # refered to x in the Test class
t.x = 3  # assigned 3 to x that is in the object t
print(t.x)  # referred to x in the object t
del t.x  # deleted x that is in the object t
print(t.x)  # referred to x in the Test class


# %% decorator
#


def bonjour(f):
    def inner(nom, *args, **kwargs):
        print("bonjour")
        f(nom, *args, **kwargs)

    return inner


@bonjour
def saluer(nom):
    print(f"Je m'appelle {nom}")


saluer("Bob")  # Bonjour
# Je m'appelle Bob


def double_resultat(f):
    def inner(n, *args, **kwargs):
        result = f(n) * 2
        return result

    return inner


@double_resultat
def carre(n):
    return n * n


print(carre(5))  # 50


def repeter(n):
    def dec(f):
        def inner():
            for _ in range(n):
                f()

        return inner

    return dec


@repeter(3)
def saluer():
    print("Salut !")


saluer()
# Salut!
# Salut!
# Salut!


# %%
import pytest


@pytest.fixture
def example_people_data():
    return [
        {
            "given_name": "Alfonsa",
            "family_name": "Ruiz",
            "title": "Senior Software Engineer",
        },
        {
            "given_name": "Sayid",
            "family_name": "Khan",
            "title": "Project Manager",
        },
    ]


def format_data_for_display(data):
    return [
        "Alfonsa Ruiz: Senior Software Engineer",
        "Sayid Khan: Project Manager",
    ]


def format_data_for_excel(data):
    return """given,family,title
Alfonsa,Ruiz,Senior Software Engineer
Sayid,Khan,Project Manager
"""


def test_format_data_for_display(example_people_data):
    assert format_data_for_display(example_people_data) == [
        "Alfonsa Ruiz: Senior Software Engineer",
        "Sayid Khan: Project Manager",
    ]


def test_format_data_for_excel(example_people_data):
    assert (
        format_data_for_excel(example_people_data)
        == """given,family,title
Alfonsa,Ruiz,Senior Software Engineer
Sayid,Khan,Project Manager
"""
    )
