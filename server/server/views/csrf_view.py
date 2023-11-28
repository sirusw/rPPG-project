from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def set_csrf_token(request):
    """
    This view sets the CSRF token for clients, allowing them to make POST requests.
    """
    return JsonResponse({"details": "CSRF cookie set"})