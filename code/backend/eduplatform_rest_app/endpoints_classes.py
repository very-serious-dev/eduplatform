import json
from django.http import JsonResponse
from .models import EPUser, EPClass, EPUserClass, EPGroup
from .models import EPUSER_STUDENT, EPUSER_TEACHER, EPUSER_TEACHER_SYSADMIN, EPUSER_TEACHER_LEADER
from .serializers import classes_array_to_json, users_array_to_json

def handle_classes(request):
    if request.method == "GET":
        if request.user is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        users_classes = EPUserClass.objects.filter(user=request.user, classroom__archived=False)
        classes = list(map(lambda uc: uc.classroom, users_classes))
        return JsonResponse({"classes": classes_array_to_json(classes)})
    elif request.method == "POST":
        if request.user is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        if request.user.role not in [EPUSER_TEACHER, EPUSER_TEACHER_SYSADMIN, EPUSER_TEACHER_LEADER]:
            return JsonResponse({"error": "No tienes permisos suficientes"}, status=403)
        try:
            body_json = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la petición incorrecto"}, status=400)
        json_name = body_json.get("name")
        json_group = body_json.get("group")
        json_automatically_add_teacher = body_json.get("automaticallyAddTeacher")
        if json_name is None or json_group is None:
            return JsonResponse({"error": "Falta name o group en el cuerpo de la petición"}, status=400)
        if EPGroup.objects.filter(tag=json_group).exists() == False:
            return JsonResponse({"error": "El grupo indicado al que debe pertenecer la clase no existe"}, status=409)
        new_class = EPClass()
        new_class.name = json_name
        new_class.group = EPGroup.objects.get(tag=json_group)
        new_class.save()
        if json_automatically_add_teacher is True:
            new_user_class = EPUserClass()
            new_user_class.user = request.user
            new_user_class.classroom = new_class
            new_user_class.save()
        # TO-DO: Feature: Automatically add to the new class all users belonging to group
        return JsonResponse({"success": True}, status=201)
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)
        
def handle_class_detail(request, classId):
    if request.method == "GET":
        if request.user is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            classroom = EPClass.objects.get(id=classId)
        except EPClass.DoesNotExist:
            return JsonResponse({"error": "La clase que buscas no existe"}, status=404)
        if request.user.role not in [EPUSER_TEACHER, EPUSER_TEACHER_SYSADMIN, EPUSER_TEACHER_LEADER]:
            isClassEditableByUser = False
        else:
            isClassEditableByUser = EPUserClass.objects.filter(user=request.user, classroom=classroom).count() > 0
        
        # TO-DO: Mock!
        response = JsonResponse({"id": classId,
                                 "name": classroom.name,
                                 "entries": [{"published_date": "2024-09-17 11:31",
                                              "author": "Test",
                                              "content": "Mañana en clase hablaremos de las fechas de los exámenes parciales"}, 
                                              {"published_date": "2024-09-14 07:42",
                                              "author": "Test",
                                              "content": "Por favor, enviadme un mensaje el número de serie de vuestro ordenador. Para sacar el número de serie, podéis ejecutar\n\n>wmic bios get serialnumber\n\n...desde un terminal. ¡Un saludo!"}, 
                                              {"published_date": "2024-09-12 14:30",
                                              "author": "Test",
                                              "content": "El centro permanecerá cerrado por festivo el próximo 7 de octubre"}, 
                                              {"published_date": "2024-09-12 09:41",
                                              "author": "Test",
                                              "content": "Recordad solicitar las habilitaciones para:\n\n- FOL\n- EIE\n\n¡Gracias!"}, 
                                              {"published_date": "2024-09-12 09:45",
                                              "author": "Test",
                                              "content": "La plataforma de Classroom dejará de funcionar próximamente.\nPor favor, pasad todos vuestros datos a Eduplatform"}, 
                                              {"published_date": "2024-09-11 08:30",
                                              "author": "Test",
                                              "content": "¡Da comienzo el nuevo curso! ¡Bienvenidos! Recordad que las clases empiezan el próximo lunes"}],
                                 "shouldShowEditButton": isClassEditableByUser })
        return response  
    elif request.method == "PUT":
        if request.user is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            classroom = EPClass.objects.get(id=classId)
        except EPClass.DoesNotExist:
            return JsonResponse({"error": "La clase que buscas no existe"}, status=404)
        if request.user.role not in [EPUSER_TEACHER, EPUSER_TEACHER_SYSADMIN, EPUSER_TEACHER_LEADER]:
            # Student - can't edit classes
            return JsonResponse({"error": "No tienes permisos para llevar a cabo esa acción"}, status=403)
        if request.user.role == EPUSER_TEACHER and EPUserClass.objects.filter(user=user, classroom=classroom).count() == 0:
            # Regular teacher trying to edit another teacher's class
            return JsonResponse({"error": "No tienes permisos para llevar a cabo esa acción"}, status=403)
        try:
            body_json = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la petición incorrecto"}, status=400)
        json_name = body_json.get("name")
        if json_name is None:
            return JsonResponse({"error": "Falta name en el cuerpo de la petición"}, status=400)
        classroom.name = json_name
        classroom.save()
        return JsonResponse({"success": True}, status=200)
    elif request.method == "DELETE":
        if request.user is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            classroom = EPClass.objects.get(id=classId)
        except EPClass.DoesNotExist:
            return JsonResponse({"error": "La clase que buscas no existe"}, status=404)
        if request.user.role not in [EPUSER_TEACHER, EPUSER_TEACHER_SYSADMIN, EPUSER_TEACHER_LEADER]:
            # Student - can't edit classes
            return JsonResponse({"error": "No tienes permisos para llevar a cabo esa acción"}, status=403)
        if request.user.role == EPUSER_TEACHER and EPUserClass.objects.filter(user=user, classroom=classroom).count() == 0:
            # Regular teacher trying to edit another teacher's class
            return JsonResponse({"error": "No tienes permisos para llevar a cabo esa acción"}, status=403)
        classroom.archived = True
        classroom.save()
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)

def handle_class_participants(request, classId):
    if request.method == "GET":
        if request.user is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            classroom = EPClass.objects.get(id=classId)
        except EPClass.DoesNotExist:
            return JsonResponse({"error": "La clase que buscas no existe"}, status=404)
        users_class = EPUserClass.objects.filter(classroom=classroom)
        if request.user.role in [EPUSER_TEACHER_SYSADMIN, EPUSER_TEACHER_LEADER]:
            has_permission_to_see = True
        else:
            has_permission_to_see = user_class.filter(user=request.user).exists()
        if not(has_permission_to_see):
            return JsonResponse({"error": "No tienes permisos suficientes"}, status=403)
        users = list(map(lambda uc: uc.user, users_class))
        return JsonResponse({"users": users_array_to_json(users)}, status=200)
    elif request.method == "PUT":
        if request.user is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            classroom = EPClass.objects.get(id=classId)
        except EPClass.DoesNotExist:
            return JsonResponse({"error": "La clase que buscas no existe"}, status=404)
        if request.user.role == EPUSER_STUDENT:
            has_permission_to_edit = False
        elif request.user.role in [EPUSER_TEACHER_SYSADMIN, EPUSER_TEACHER_LEADER]:
            has_permission_to_edit = True
        else: # Regular teacher
            has_permission_to_edit = EPUserClass.objects.filter(classroom=classroom, user=request.user).exists()
        if not(has_permission_to_edit):
            return JsonResponse({"error": "No tienes permisos suficientes"}, status=403)
        try:
            body_json = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la petición incorrecto"}, status=400)
        json_username = body_json.get("username")
        if json_username is None:
            return JsonResponse({"error": "Falta username en el cuerpo de la petición"}, status=400)
        failed_inexistent_users = []
        failed_already_added_users = []
        for non_trimmed_username in json_username.split(","):
            username = non_trimmed_username.strip()
            if len(username) > 0:
                try:
                    user = EPUser.objects.get(username=username)
                    if EPUserClass.objects.filter(user=user, classroom=classroom).exists():
                        failed_already_added_users.append(username)
                    else:
                        new_user_class = EPUserClass()
                        new_user_class.user = user
                        new_user_class.classroom = classroom
                        new_user_class.save()
                except EPUser.DoesNotExist:
                    failed_inexistent_users.append(username)
        if len(failed_inexistent_users) == 0 and (failed_already_added_users) == 0:
            return JsonResponse({"success": True}, status=201)
        else:
            error_msg = ""
            if len(failed_inexistent_users) > 0:
                error_msg += "Usuario(s) inexistente(s): " + ", ".join(failed_inexistent_users) + ". "
            if len(failed_already_added_users) > 0:
                error_msg += "Usuario(s) ya pertenece(n) a la clase: " + ", ".join(failed_already_added_users)
            return JsonResponse({"partial_success": True, "error": error_msg}, status=201)
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)

def handle_class_participant_deletion(request, classId, username):
    if request.method == "DELETE":
        if request.user is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            classroom = EPClass.objects.get(id=classId)
        except EPClass.DoesNotExist:
            return JsonResponse({"error": "La clase que buscas no existe"}, status=404)
        if request.user.role == EPUSER_STUDENT:
            has_permission_to_edit = False
        elif request.user.role in [EPUSER_TEACHER_SYSADMIN, EPUSER_TEACHER_LEADER]:
            has_permission_to_edit = True
        else: # Regular teacher
            has_permission_to_edit = EPUserClass.objects.filter(classroom=classroom, user=request.user).exists()
        if not(has_permission_to_edit):
            return JsonResponse({"error": "No tienes permisos suficientes"}, status=403)
        try:
            user_class = EPUserClass.objects.get(classroom=classroom, user__username=username)
            user_class.delete()
            return JsonResponse({"success": True}, status=200)
        except EPUserClass.DoesNotExist:
            return JsonResponse({"error": "El usuario no pertenece a esa clase"}, status=404)
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)
