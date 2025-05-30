import json
from datetime import datetime
from django.http import JsonResponse
from .models import User, Group, Announcement, Folder, AnnouncementDocument, Document
from .serializers import groups_array_to_json, announcements_array_to_json
from .endpoints_posts import POSTS_DOCUMENTS_ROOT_FOLDER_NAME

def get_all_groups(request):
    if request.method == "GET":
        if request.session is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        groups = Group.objects.all()
        return JsonResponse({"groups": groups_array_to_json(groups) })  
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)

def handle_group_announcements(request, groupTag):
    if request.method == "GET":
        if request.session is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            group = Group.objects.get(tag=groupTag)
        except Group.DoesNotExist:
            return JsonResponse({"error": "Ese grupo no existe"}, status=404)
        if request.session.user.role in [User.UserRole.TEACHER_SYSADMIN, User.UserRole.TEACHER_LEADER]:
            canSee = True
            canCreate = True
        elif request.session.user.role in [User.UserRole.TEACHER]:
            canSee = True # All teachers can access all announcements boards
            canCreate = group.tutor == request.session.user
        else:
            canSee = request.session.user.student_group == group
            canCreate = False
        if not canSee:
            return JsonResponse({"error": "No tienes permisos suficientes"}, status=403)
        announcements = Announcement.objects.filter(group=group).order_by("-publication_date")
        return JsonResponse({"success": True,
                             "announcements": announcements_array_to_json(announcements),
                             "can_create_announcements": canCreate})
    elif request.method == "POST":
        if request.session is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            group = Group.objects.get(tag=groupTag)
        except Group.DoesNotExist:
            return JsonResponse({"error": "Ese grupo no existe"}, status=404)
        if request.session.user.role in [User.UserRole.TEACHER_SYSADMIN, User.UserRole.TEACHER_LEADER]:
            hasPermission = True
        elif request.session.user.role in [User.UserRole.TEACHER]:
            hasPermission = group.tutor == request.session.user
        else:
            hasPermission = False
        if not hasPermission:
            return JsonResponse({"error": "No tienes permisos suficientes"}, status=403)
        try:
            body_json = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la petición incorrecto"}, status=400)
        json_title = body_json.get("title")
        json_content = body_json.get("content")
        json_files = body_json.get("files")
        if json_title is None or json_content is None or json_files is None:
            return JsonResponse({"error": "Falta title, content o files en el cuerpo de la petición"}, status=400)
        new_announcement = Announcement()
        new_announcement.title = json_title
        new_announcement.content = json_content
        new_announcement.author = request.session.user
        new_announcement.group = group
        new_announcement.save()
        if len(json_files) > 0:
            # Create parent folders if they don't exist
            try:
                posts_docs_root_folder = Folder.objects.get(author=request.session.user, name=POSTS_DOCUMENTS_ROOT_FOLDER_NAME, is_autogenerated=True)
            except Folder.DoesNotExist:
                posts_docs_root_folder = Folder()
                posts_docs_root_folder.author = request.session.user
                posts_docs_root_folder.name = POSTS_DOCUMENTS_ROOT_FOLDER_NAME
                posts_docs_root_folder.is_autogenerated = True
                posts_docs_root_folder.save()
            try:
                folder_name = __folder_name_for_group(group)
                group_announcements_folder = Folder.objects.get(author=request.session.user, name=folder_name, parent_folder=posts_docs_root_folder, is_autogenerated=True)
            except Folder.DoesNotExist:
                group_announcements_folder = Folder()
                group_announcements_folder.author = request.session.user
                group_announcements_folder.name = folder_name
                group_announcements_folder.parent_folder=posts_docs_root_folder
                group_announcements_folder.is_autogenerated = True
                group_announcements_folder.save()
        for f in json_files:
            document = Document()
            document.identifier = f["identifier"]
            document.name = f["name"]
            document.size = f["size"]
            document.mime_type = f["mime_type"]
            document.author = request.session.user
            document.folder = group_announcements_folder
            document.is_protected = True
            document.save()
            announcement_document = AnnouncementDocument()
            announcement_document.document = document
            announcement_document.announcement = new_announcement
            announcement_document.save()
        return JsonResponse({"success": True}, status=201)
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)

def handle_announcement(request, announcementId):
    if request.method == "DELETE":
        if request.session is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            announcement = Announcement.objects.get(id=announcementId)
        except Announcement.DoesNotExist:
            return JsonResponse({"error": "Ese anuncio no existe"}, status=404)
        if request.session.user.role in [User.UserRole.TEACHER_SYSADMIN, User.UserRole.TEACHER_LEADER]:
            hasPermission = True
        elif request.session.user.role in [User.UserRole.TEACHER]:
            hasPermission = group.tutor == request.session.user
        else:
            hasPermission = False
        if not hasPermission:
            return JsonResponse({"error": "No tienes permisos suficientes"}, status=403)
        announcement.delete()
        return JsonResponse({"success": True}, status=201)
    elif request.method == "PUT":
        if request.session is None:
            return JsonResponse({"error": "Tu sesión no existe o ha caducado"}, status=401)
        try:
            announcement = Announcement.objects.get(id=announcementId)
        except Announcement.DoesNotExist:
            return JsonResponse({"error": "Ese anuncio no existe"}, status=404)
        if request.session.user.role in [User.UserRole.TEACHER_SYSADMIN, User.UserRole.TEACHER_LEADER]:
            hasPermission = True
        elif request.session.user.role in [User.UserRole.TEACHER]:
            hasPermission = group.tutor == request.session.user
        else:
            hasPermission = False
        if not hasPermission:
            return JsonResponse({"error": "No tienes permisos suficientes"}, status=403)
        try:
            body_json = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la petición incorrecto"}, status=400)
        json_title = body_json.get("title")
        json_content = body_json.get("content")
        json_files = body_json.get("files")
        if json_title is None or json_content is None or json_files is None:
            return JsonResponse({"error": "Falta title, content o files en el cuerpo de la petición"}, status=400)
        announcement.title = json_title
        announcement.content = json_content
        announcement.modification_date = datetime.now() # FIXME: The datetime stored is wrong - RuntimeWarning: DateTimeField Announcement.modification_date received a naive datetime (2025-04-13 01:27:04.149266) while time zone support is active.
        announcement.save()
        # Remove previous files
        announcement_documents = AnnouncementDocument.objects.filter(announcement=announcement)
        announcement_documents.delete()
        
        for f in json_files:
            try:
                document = Document.objects.get(identifier=f["identifier"])
            except Document.DoesNotExist:
                group_folder_name = __folder_name_for_group(announcement.group)
                try:
                    posts_docs_root_folder = Folder.objects.get(author=request.session.user, name=POSTS_DOCUMENTS_ROOT_FOLDER_NAME, is_autogenerated=True)
                    group_folder = Folder.objects.get(author=request.session.user, name=group_folder_name, parent_folder=posts_docs_root_folder, is_autogenerated=True)
                except Folder.DoesNotExist:
                    return JsonResponse({}, status=500) # This should never happen, the announcement is being edited and the folder was previously autogenerated
                document = Document()
                document.identifier = f["identifier"]
                document.name = f["name"]
                document.size = f["size"]
                document.mime_type = f["mime_type"]
                document.author = request.session.user
                document.folder = group_folder
                document.is_protected = True
                document.save()
            announcement_document = AnnouncementDocument()
            announcement_document.document = document
            announcement_document.announcement = announcement
            announcement_document.save()
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"error": "Unsupported"}, status=405)

def __folder_name_for_group(group):
    return group.tag
