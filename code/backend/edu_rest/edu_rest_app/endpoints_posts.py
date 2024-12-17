import json
from django.http import JsonResponse
from .models import Class, UserClass, Unit, Post, Document, PostDocument
from .models import USER_STUDENT, USER_TEACHER, USER_TEACHER_SYSADMIN, USER_TEACHER_LEADER, POST_PUBLICATION, POST_TASK
from .serializers import assignment_to_json

def create_post(request, classId):
    if request.method == "POST":
        if request.session is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            classroom = Class.objects.get(id=classId)
        except Class.DoesNotExist:
            return JsonResponse({"error": "La clase que buscas no existe"}, status=404)
        if request.session.user.role not in [USER_TEACHER, USER_TEACHER_SYSADMIN, USER_TEACHER_LEADER]:
            # Student - can't create posts inside a class
            return JsonResponse({"error": "No tienes permisos para llevar a cabo esa acción"}, status=403)
        if request.session.user.role == USER_TEACHER and UserClass.objects.filter(user=request.session.user, classroom=classroom).count() == 0:
            # Regular teacher trying to post on another teacher's class
            return JsonResponse({"error": "No tienes permisos para llevar a cabo esa acción"}, status=403)
        try:
            body_json = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la petición incorrecto"}, status=400)
        json_title = body_json.get("title")
        json_unit_id = body_json.get("unit_id")
        json_content = body_json.get("content")
        json_post_type = body_json.get("post_type")
        json_task_due_date = body_json.get("task_due_date")
        json_files = body_json.get("files")
        if json_title is None or json_content is None or json_post_type is None:
            return JsonResponse({"error": "Falta title, content o post_type en el cuerpo de la petición"}, status=400)
        if json_post_type not in ["publication", "task"]:
            return JsonResponse({"error": "post_type inválido"}, status=400)
        if json_unit_id is None:
            unit = None
        else:
            try:
                unit = Unit.objects.get(id=json_unit_id)
            except Unit.DoesNotExist:
                return JsonResponse({"error": "No existe un tema con ese id"}, status=404)
        new_post = Post()
        new_post.title = json_title
        new_post.content = json_content
        new_post.unit = unit
        new_post.classroom = classroom
        new_post.author = request.session.user
        if json_post_type == "publication":
            new_post.kind = POST_PUBLICATION
        elif json_post_type == "task":
            new_post.kind = POST_TASK
            if json_task_due_date is not None:
                new_post.task_due_date = json_task_due_date
        new_post.save()
        if json_files is not None:
            for f in json_files:
                document = Document()
                document.identifier = f["identifier"]
                document.name = f["name"]
                document.size = f["size"]
                document.mime_type = f["mime_type"]
                document.author = request.session.user
                document.save()
                post_document = PostDocument()
                post_document.document = document
                post_document.post = new_post
                post_document.save()
        return JsonResponse({"success": True}, status=201) 
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)

def assignment_detail(request, assignmentId):
    if request.method == "GET":
        if request.session is None: # FIX-ME: So much CTRL+C CTRL+V :(
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            assignment = Post.objects.get(id=assignmentId, kind=POST_TASK)
        except Post.DoesNotExist:
            return JsonResponse({"error": "La tarea que buscas no existe"}, status=404)
        if request.session.user.role not in [USER_TEACHER, USER_TEACHER_SYSADMIN, USER_TEACHER_LEADER]:
            # Student - can't globally view assignments
            return JsonResponse({"error": "No tienes permisos para llevar a cabo esa acción"}, status=403)
        if request.session.user.role == USER_TEACHER and UserClass.objects.filter(user=request.session.user, classroom=assignment.classroom).count() == 0:
            # Regular teacher trying to view another teacher's class assignment
            return JsonResponse({"error": "No tienes permisos para llevar a cabo esa acción"}, status=403)
        
        # TODO Return also tasksubmit documents
        return JsonResponse(assignment_to_json(assignment)) 
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)
    
