class BadRequest(Exception):
    pass

class BadRequestInvalidPassword(Exception):
    pass

class BadRequestInvalidUsername(Exception):
    pass

class BadRequestInvalidTag(Exception):
    pass

class BadRequestInvalidYear(Exception):
    pass

class BadRequestIllegalMove(Exception):
    pass
    
class Unauthorized(Exception):
    pass

class UnauthorizedIncorrectPassword(Exception):
    pass

class Forbidden(Exception):
    pass

class ForbiddenAlreadyAnswered(Exception):
    pass

class ForbiddenAssignmentSubmit(Exception):
    pass

class ForbiddenEditHasAnswers(Exception):
    pass

class ForbiddenExceededLoginAttempts(Exception):
    pass

class ForbiddenQuestionnaireAssignmentIsDue(Exception):
    pass

class ForbiddenQuestionnaireAssignmentIsNotDue(Exception):
    pass

class NotFound(Exception):
    pass

class Unsupported(Exception):
    pass

class ConflictFolderAlreadyExists(Exception):
    pass

class ConflictGroupAlreadyExists(Exception):
    pass

class ConflictQuotaExceeded(Exception):
    pass

class ConflictUnitAlreadyExists(Exception):
    pass

class ConflictUserAlreadyExists(Exception):
    pass

class InternalError(Exception):
    pass
