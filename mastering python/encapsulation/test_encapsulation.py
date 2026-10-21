import unittest

from encapsulation import Product, PriceError, ProductNameError


class TestProduct(unittest.TestCase):
    def test_create_product_success(self):
        """
        Test The creation of a product,
        """
        laptop = Product(
            name="laptop dell",
            price=750,
        )
        self.assertIsInstance(laptop, Product)
        self.assertEqual(laptop.name, "laptop dell")
        self.assertEqual(laptop.price, 750)

    def test_create_product_fail(self):
        """
        Test create product fail
        """
        with self.assertRaises(PriceError):
            _ = Product(
                name="smartphone",
                price=-200,
            )

        with self.assertRaises(PriceError):
            _ = Product(
                "phone",
                0,
            )

        with self.assertRaises(ProductNameError):
            _ = Product(
                "",
                1400,
            )

        with self.assertRaises(TypeError):
            _ = Product(
                False,
                500,
            )

    def test_update_product_price_fail(self):
        """
        Test that updating the product price with inappropriate price will fail
        """
        monitor = Product(
            "acer monitor",
            600,
        )

        with self.assertRaises(PriceError):
            monitor.price = -150

        with self.assertRaises(TypeError):
            monitor.price = "test"

    def test_update_product_name_fail(self):
        """
        Test that updating a product name with an inappropriate value will fail
        """
        chair = Product(
            "chair ergo",
            300,
        )
        with self.assertRaises(ProductNameError):
            chair.name = ""

        with self.assertRaises(TypeError):
            chair.name = False


if __name__ == "__main__":
    unittest.main()
