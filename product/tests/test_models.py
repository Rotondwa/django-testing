from django.test import TestCase
from django.core.exceptions import ValidationError
from product.models import Product

# Create your tests here.
class TestProductModel(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100.00, stock_count=10)


    def test_in_stock_property(self):
        self.assertTrue(self.product.in_stock)

        # set the stock count to 0
        self.product.stock_count = 0
        self.assertFalse(self.product.in_stock)

    def test_get_discounted_price(self):
        self.assertEqual(self.product.get_discounted_price(10), 90.00)
        self.assertEqual(self.product.get_discounted_price(50), 50.00)
        self.assertEqual(self.product.get_discounted_price(0), 100.00)

    def test_negative_price_raises_validation_error(self):
        self.product.price = -10.00
        with self.assertRaises(ValidationError):
            self.product.clean()

    def test_negative_stock_count_raises_validation_error(self):
        self.product.stock_count = -10
        with self.assertRaises(ValidationError):
            self.product.clean()