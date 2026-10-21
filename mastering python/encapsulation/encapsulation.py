"""
learning Encapsulation:
- the main goal of this exerise is implement a robust class Computer, that protect it's internal attributes from the miss use of the client/external code
- goals:
    - work following TDD
    - clean readable code
    - maintainable code
    - clean well written doc strings
"""


class PriceError(ValueError):
    def __init__(self):
        self.message = "Price must be >= 0"

class ProductNameError(ValueError):
    def __init__(self):
        self.message = "name must not be an empty string"

class Product:
    def __init__(self, name: str, price: int | float) -> None:
        """
        - Initialiase a product with a name and a price
        - Raises: `TypeError` if attributes are the wrong type, `PriceError` if the price <= 0, `ProductNameError` if name is empty string
        ### Example:
        ```python
        laptop = Product(
            "laptop hp",
            1200,
        )
        ```
        """
        if not isinstance(name, str):
            raise TypeError("name must be an str")
        if not isinstance(price, (int, float)):
            raise TypeError("price must be an int | float")
        if not name:
            raise ProductNameError()
        if price <= 0:
            raise PriceError()

        self._name = name
        self._price = price

    @property
    def name(self) -> str:
        """
        Expose the internal name
        """
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """
        Update the product with a new name
        Raises: `TypeError` if new_name is not an str,  `ValueError` if new_name is an empty str
        """
        if not isinstance(new_name, str):
            raise TypeError("new_name must be an str")
        if not new_name:
            raise ProductNameError()
        self._name = new_name

    @property
    def price(self) -> int | float:
        """
        Expose the internal price
        """
        return self._price

    @price.setter
    def price(self, new_price: int | float) -> None:
        """
        Update the price with a new one
        Raises: `ValueError` if price <= 0, TypeError if new_price is not an int | float
        """
        if not isinstance(new_price, (int, float)):
            raise TypeError("Price must be an int or a float")
        if new_price <= 0:
            raise PriceError
        self._price = new_price