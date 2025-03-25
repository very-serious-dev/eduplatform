import json, requests, secrets, socket
import requests.packages.urllib3.util.connection as urllib3_cn
from django.http import JsonResponse
from .middleware_auth import AUTH_COOKIE_KEY
from .models import UserSession
from .internal_secret import INTERNAL_SECRET

# Force IPv4 on requests library to improve connection speed
# https://stackoverflow.com/a/46972341
def allowed_gai_family_override():
    return socket.AF_INET
urllib3_cn.allowed_gai_family = allowed_gai_family_override


EDU_REST_INTERNAL_BASE_URL = "http://localhost:8002"
EDU_REST_INTERNAL_VERIFY_SESSION_ENDPOINT = "/internal/v1/sessions"

def login_logout(request):
    if request.method == "POST":
        try:
            body_json = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la petición incorrecto"}, status=400)
        json_one_time_token = body_json.get("one_time_token")
        if json_one_time_token is None:
            return JsonResponse({"error": "Falta one_time_token en el cuerpo de la petición"}, status=400)
        verify_identity_request_body = { "internal_secret": INTERNAL_SECRET, "one_time_token": json_one_time_token }
        edu_rest_response = requests.post(EDU_REST_INTERNAL_BASE_URL + EDU_REST_INTERNAL_VERIFY_SESSION_ENDPOINT, json=verify_identity_request_body)
        if edu_rest_response.status_code != 200:
            return JsonResponse({"error": "Error verificando identidad"}, status=502)
        try:
            edu_rest_json_response = edu_rest_response.json()
            json_edu_rest_user_id = edu_rest_json_response["user_id"]
        except (requests.JSONDecodeError, KeyError):
            return JsonResponse({"error": "Error verificando identidad"}, status=502)
        # Let's create a new session
        random_token = secrets.token_hex(20)
        session = UserSession()
        session.user_id = json_edu_rest_user_id
        session.token = random_token
        session.save()
        response = JsonResponse({"success": True}, status=201)
        response.set_cookie(key=AUTH_COOKIE_KEY, value=random_token, path="/", samesite="Strict", httponly=True) # TO-DO: Should be secure=True too when using HTTPS
        return response
    elif request.method == "DELETE":
        if request.session is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        request.session.delete()
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)
