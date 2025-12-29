import jwt
from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from .models import User

def jwt_required(view_func):
    """Decorator to protect views with JWT authentication"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return JsonResponse({"status": False, "message": "Authorization required"}, status=401)

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
            request.user_email = payload['user_email']
            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"status": False, "message": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"status": False, "message": "Invalid token"}, status=401)

    return wrapper

def get_user_from_token(request):
    """Get user from JWT token"""
    auth_header = request.headers.get('Authorization', '')

    if not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return User.objects.get(id=payload['user_id'])
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return None

