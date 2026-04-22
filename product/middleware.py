from django.http import HttpResponse
from django.conf import settings

class MaintenanceMiddleware:
    """
     Middleware that checks if the site is in maintenance mode
     If the MAINTENANCE_MODE is set to True, it returns a Service Unavailable response
     """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'MAINTENANCE_MODE', False):
            return HttpResponse('Site is under maintenance', status=503)
        return self.get_response(request)









    