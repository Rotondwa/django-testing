from sqlite3 import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from product.models import Product
from django.db import IntegrityError

# Create your tests here.
class TestProductModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(name="Test Product", price=100.00, stock_count=10)


    def test_in_stock_property(self):
        self.assertTrue(self.product.in_stock)

        # set the stock count to 0
        self.product.stock_count = 0
        self.assertFalse(self.product.in_stock)

    def test_get_discounted_price(self):
        self.assertEqual(self.product.get_discounted_price(10), 90.00)
        self.assertEqual(self.product.get_discounted_price(50), 50.00)
        self.assertEqual(self.product.get_discounted_price(0), 100.00)

    # def test_negative_price_raises_validation_error(self):
    #     self.product.price = -10.00
    #     with self.assertRaises(ValidationError):
    #         self.product.clean()

    # def test_negative_stock_count_raises_validation_error(self):
    #     self.product.stock_count = -10
    #     with self.assertRaises(ValidationError):
    #         self.product.clean()

    def test_negative_price_constraint_raises_integrity_error(self):
        self.product.price = -10.00
        with self.assertRaises(IntegrityError):
            self.product.save()

    def test_negative_stock_count_constraint_raises_integrity_error(self):
        self.product.stock_count = -10
        with self.assertRaises(IntegrityError):
            self.product.save()

    # Edge case test
    def test_edge_case_product_creation(self):
        product = Product.objects.create(name="Test Product", price=0.00, stock_count=0)
        self.assertEqual(product.price, 0.00)
        self.assertEqual(product.stock_count, 0)
        self.assertFalse(product.in_stock)
        self.assertEqual(product.get_discounted_price(10), 0.00)
        self.assertEqual(product.get_discounted_price(50), 0.00)
        self.assertEqual(product.get_discounted_price(0), 0.00)