from django.urls import path

from . import endpoints_sessions, endpoints_documents

urlpatterns = [
    path("sessions", endpoints_sessions.login_logout),
    path("documents", endpoints_documents.create_or_delete_documents),
    path("documents/<identifier>", endpoints_documents.get_document)
]
