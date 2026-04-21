from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from product.models import Product, User


class TestProfilePage(TestCase):

    def test_profile_view_redirects_for_anonymous_users(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, expected_url=f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_view_accessible_for_authenticated_users(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Login the user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))

        # Check that the user is redirected to the login page
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'Your Profile')
        

class TestHomePageView(SimpleTestCase):

    # def test_homepage_status_code(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)

    def test_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

    def test_homepage_contains_welcome_message(self):
        response = self.client.get('/')
        self.assertContains(response, 'Welcome to the homepage', status_code=200)


""" Since we now want to access the products page, we need to create a test for that using TestCase instead of SimpleTestCase.
This is because we need to access the database to get the products.
"""
class TestProductsPage(TestCase):

    def setUp(self):
        Product.objects.create(name="Test Product", price=100.00, stock_count=10)
        Product.objects.create(name="Test Product 2", price=200.00, stock_count=20)
        Product.objects.create(name="Test Product 3", price=300.00, stock_count=30)

    def test_products_uses_correct_template(self):
        response = self.client.get(reverse('products'))
        self.assertTemplateUsed(response, 'products.html')

    def test_products_context(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(len(response.context['products']), 3)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'Test Product 2')
        self.assertContains(response, 'Test Product 3')
        self.assertNotContains(response, 'No products found')

    def test_products_view_no_products(self):
        Product.objects.all().delete()
        response = self.client.get(reverse('products'))
        self.assertContains(response, 'No products found')
        self.assertEqual(len(response.context['products']), 0)
        

    # def test_products_contains_correct_html(self):
    #     response = self.client.get(reverse('products'))
    #     self.assertContains(response, 'Products', status_code=200)
    #     self.assertContains(response, 'Test Product', status_code=200)
    #     self.assertContains(response, 'Test Product 2', status_code=200)
    #     self.assertContains(response, 'Test Product 3', status_code=200)
        