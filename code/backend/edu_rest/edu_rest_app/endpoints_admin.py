import bcrypt, json, re
from django.http import JsonResponse
from django.db.models import Q
from .models import User, Group, Class, UserClass, UserSession
from .serializers import groups_array_to_json, classes_array_to_json, users_array_to_json
from .admin_secret import ADMIN_SECRET

def home(request):
    if request.method == "GET":
        admin_auth_error = __admin_auth_json_error_response(request)
        if admin_auth_error is not None:
            return admin_auth_error
        users_count = User.objects.all().count()
        classes_count = Class.objects.filter(archived=False).count()
        serialized_groups = []
        groups = Group.objects.all()
        return JsonResponse({"usersCount": users_count,
                             "classesCount": classes_count,
                             "groups": groups_array_to_json(groups) })
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)
    
def create_user(request):
    if request.method == "POST":
        admin_auth_error = __admin_auth_json_error_response(request)
        if admin_auth_error is not None:
            return admin_auth_error
        try:
            body_json = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la petición incorrecto"}, status=400)
        json_username = body_json.get("username")
        json_name = body_json.get("name")
        json_surname = body_json.get("surname")
        json_password = body_json.get("password")
        json_student_group = body_json.get("student_group")
        json_is_teacher = body_json.get("is_teacher", False)
        if json_username is None or json_name is None or json_surname is None or json_password is None:
            return JsonResponse({"error": "Falta username, name, surname o password en el cuerpo de la petición"}, status=400)
        if not(re.match("^[a-z0-9.]+$", json_username)):
            return JsonResponse({"error": "El nombre de usuario no es válido. Sólo puede contener letras en minúscula, dígitos y puntos (.)"}, status=409)
        if User.objects.filter(username=json_username).exists():
            return JsonResponse({"error": "Ese usuario ya está registrado"}, status=409)
        new_user = User()
        new_user.username = json_username
        new_user.name = json_name
        new_user.surname = json_surname
        new_user.encrypted_password = bcrypt.hashpw(json_password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
        if json_is_teacher:
            new_user.role = User.UserRole.TEACHER
        elif json_student_group is not None:
            try:
                group = Group.objects.get(tag=json_student_group)
            except Group.DoesNotExist:
                return JsonResponse({"error": "El grupo especificado no existe"}, status=409)
            new_user.role = User.UserRole.STUDENT
            new_user.student_group = group
        else:
            # School leader and Sysadmin must be manually added
            # Thus, if execution reaches here, request was incorrect
            return JsonResponse({"error": "Falta student_group o is_teacher"}, status=400)
        new_user.save()
        return JsonResponse({"success": True}, status=201)
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)


def create_group(request):
    if request.method == "POST":
        admin_auth_error = __admin_auth_json_error_response(request)
        if admin_auth_error is not None:
            return admin_auth_error
        try:
            body_json = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la petición incorrecto"}, status=400)
        json_tag = body_json.get("tag")
        json_name = body_json.get("name")
        json_year = body_json.get("year")
        json_tutor_username = body_json.get("tutor_username")
        if json_tag is None or json_name is None or json_tutor_username is None or json_year is None:
            return JsonResponse({"error": "Falta tag, name, year o tutor_username en el cuerpo de la petición"}, status=400)
        if not(re.match("^[A-Za-z0-9]+$", json_tag)):
            return JsonResponse({"error": "El tag no es válido. Sólo puede contener letras y dígitos"}, status=409)
        if not(re.match("^[0-9-]+$", json_year)):
            return JsonResponse({"error": "Año inválido. Sólo puede contener dígitos y guiones"}, status=409)
        if Group.objects.filter(tag=json_tag, year=json_year).exists():
            return JsonResponse({"error": "Ese grupo ya está registrado"}, status=409)
        if User.objects.filter(username=json_tutor_username).exists() == False:
            return JsonResponse({"error": "El tutor indicado no existe"}, status=409)
        new_group = Group()
        new_group.tag = json_tag
        new_group.name = json_name
        new_group.year = json_year
        # Here we assume that json_tutor_username is a valid and correct teacher,
        # because it's chosen from a preloaded HTML <select> with the teachers
        new_group.tutor = User.objects.get(username=json_tutor_username)
        new_group.save()
        return JsonResponse({"success": True}, status=201)
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)

def get_all_classes(request):
    if request.method == "GET":
        admin_auth_error = __admin_auth_json_error_response(request)
        if admin_auth_error is not None:
            return admin_auth_error
        classes = Class.objects.filter(archived=False)
        return JsonResponse({"classes": classes_array_to_json(classes) })
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)

def get_teachers(request):
    if request.method == "GET":
        admin_auth_error = __admin_auth_json_error_response(request)
        if admin_auth_error is not None:
            return admin_auth_error
        users = User.objects.filter(Q(role=User.UserRole.TEACHER) | Q(role=User.UserRole.TEACHER_SYSADMIN) | Q(role=User.UserRole.TEACHER_LEADER))
        return JsonResponse({"teachers": users_array_to_json(users) })
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)


def verify_session(request): # This is received from another server (DocuREST); not the React client
                             # See docs/auth_flow.txt for further information
    if request.method == "POST":
        try:
            body_json = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la petición incorrecto"}, status=400)
        json_admin_secret = body_json.get("admin_secret")
        json_one_time_token = body_json.get("one_time_token")
        if json_admin_secret is None or json_one_time_token is None:
            return JsonResponse({"error": "Error"}, status=400)
        if json_admin_secret != ADMIN_SECRET:
            return JsonResponse({"error": "Error"}, status=400)
        try:
            user_session = UserSession.objects.get(one_time_token=json_one_time_token)
        except UserSession.DoesNotExist:
            return JsonResponse({"error": "Error"}, status=400)
        if user_session.one_time_token_already_used == True:
            # TODO: Implement an actual log system
            print("[SEVERE] Security warning: The one_time_token " + json_one_time_token)
            print("has been used twice in /admin/sessions. This should never happen in a regular")
            print("authentication flow. Someone might trying to do something naughty")
            user_session.delete()
            return JsonResponse({"error": "Error"}, status=400)
        user_session.one_time_token_already_used = True
        user_session.save()
        return JsonResponse({"user_id": user_session.user.id})
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)
    
def __admin_auth_json_error_response(request):
    if request.session.user is None:
        return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
    if request.session.user.role not in [User.UserRole.TEACHER_SYSADMIN, User.UserRole.TEACHER_LEADER]:
        return JsonResponse({"error": "No tienes permisos suficientes"}, status=403)
    return None
