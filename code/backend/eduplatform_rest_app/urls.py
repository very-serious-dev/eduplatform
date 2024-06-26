from django.urls import path
from . import endpoints_users, endpoints_classes, endpoints_admin

urlpatterns = [
    path("admin/home", endpoints_admin.home),
    path("admin/users", endpoints_admin.handle_users),
    path("admin/users/teachers", endpoints_admin.get_teachers),
    path("admin/groups", endpoints_admin.handle_groups),
    path("admin/classes", endpoints_admin.handle_classes),
    path("sessions", endpoints_users.handle_login),
    path("classes", endpoints_classes.handle_classes),
    path("classes/<int:classId>", endpoints_classes.handle_class_detail)
]
