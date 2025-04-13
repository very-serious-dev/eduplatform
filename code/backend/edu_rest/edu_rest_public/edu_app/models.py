from django.db import models

TOKEN_SIZE=30

##
# USERS
#

class User(models.Model):
    
    class UserRole(models.IntegerChoices):
        # Maintainability note:
        # EduREST internal API contains a is_teacher function in endpoints.py
        STUDENT = 0
        TEACHER = 1
        TEACHER_SYSADMIN = 2
        TEACHER_LEADER = 3

    username = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    encrypted_password = models.CharField(max_length=120)
    role = models.IntegerField(choices=UserRole)
    student_group = models.ForeignKey("Group", on_delete=models.SET_NULL, null=True, default=None)
    max_folders = models.IntegerField()
    max_documents = models.IntegerField()
    max_documents_size = models.IntegerField()

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Sent to client after successful login via HttpOnly Set-Cookie
    token = models.CharField(unique=True, max_length=TOKEN_SIZE)
    # Sent to client after successful login via response body (JSON)
    # See docs/auth_flow.txt for further information
    one_time_token = models.CharField(unique=True, max_length=TOKEN_SIZE)
    one_time_token_already_used = models.BooleanField(default=False)

##
# FILES
#

class Folder(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_folder = models.ForeignKey("Folder", on_delete=models.CASCADE, null=True)
    is_autogenerated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    identifier = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    size = models.IntegerField() # in bytes; safe max value is 2147483647 (=2048 MB)
    mime_type = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    is_protected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class UserDocumentPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

class UserFolderPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

##
# CLASSES
#

class Group(models.Model):
    tag = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    tutor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    year = models.CharField(max_length=10)

class Class(models.Model):

    class ClassTheme(models.IntegerChoices):
        RED = 0
        GREEN = 1
        BLUE = 2

    name = models.CharField(max_length=50)
    theme = models.IntegerField(choices=ClassTheme)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)

class UserClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)

class Unit(models.Model):
    name = models.CharField(max_length=50)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)

##
# ANNOUNCEMENTS
#

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=3000)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(default=None, null=True)
    
class AnnouncementDocument(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

##
# POSTS
#

class Post(models.Model):

    class PostKind(models.IntegerChoices):
        PUBLICATION = 0
        ASSIGNMENT = 1
        AMENDMENT_EDIT = 2
        AMENDMENT_DELETE = 3

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=3000)
    kind = models.IntegerField(choices=PostKind)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    assignment_due_date = models.DateField(null=True)
    amendment_original_post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True)

class PostDocument(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

class AssignmentSubmit(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000, null=True)
    submit_date = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True)
    is_score_published = models.BooleanField(default=False)

class AssignmentSubmitDocument(models.Model):
    submit = models.ForeignKey(AssignmentSubmit, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
