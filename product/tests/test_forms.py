from django.test import TestCase
from django.urls import reverse
from product.forms import ProductForm
from product.models import Product

class ProductFormTest(TestCase):

    def test_create_product_form_valid(self):
        """ Test that the product form is valid """
        form_data = {
            'name': 'Test Product',
            'price': 100.00,
            'stock_count': 10
        }

        response = self.client.post(reverse('products'), data=form_data)

        # check that the product was created
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='Test Product').exists())

    def test_dont_create_product_form_invalid(self):
        """ Test that the product form is invalid """
        form_data = {
            'name': '', # name is required
            'price': -100.00, # price is required
            'stock_count': -10 # stock count is required
        }
        response = self.client.post(reverse('products'), data=form_data)
        # check that the product was not created
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)

        form = response.context['form']
        self.assertFormError(form, 'name', 'This field is required.')
        self.assertFormError(form, 'price', 'Price cannot be negative')
        self.assertFormError(form, 'stock_count', 'Stock count cannot be negative')

        # Check no products were created
        self.assertFalse(Product.objects.exists())

