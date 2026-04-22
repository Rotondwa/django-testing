from django.test import TestCase, override_settings
from django.urls import reverse
from unittest.mock import patch
from django.conf import settings
from django.http import HttpResponse

class MaintenanceMiddlewareTest(TestCase):

    @override_settings(MAINTENANCE_MODE=False)
    def test_maintenance_mode_disabled(self):
        """
        Test that the middleware returns a 200 response when the maintenance mode is disabled
        """
        response = self.client.get(reverse('homepage'))

        # Check that the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to the homepage')

    
    @override_settings(MAINTENANCE_MODE=True)
    def test_maintenance_mode_enabled(self):
        """
        Test that the middleware returns a 503 response when the maintenance mode is enabled
        """
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 503)
        self.assertContains(response, 'Site is under maintenance', status_code=503)