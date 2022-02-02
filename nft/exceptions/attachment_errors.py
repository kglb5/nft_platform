import patreon
from patreon.constants.http_codes import REQUEST_ENTITY_TOO_LARGE_413
from patreon.exception import APIException, ParameterMissing, ResourceMissing, \
    ViewForbidden, EditForbidden


class AttachmentIDsMissing(ParameterMissing):
    parameter_name = 'ids'


class FileTooLarge(APIException):
    status_code = REQUEST_ENTITY_TOO_LARGE_413
    error_title = "Uploaded file is too large. Max file size is {}MB.".format(
        int(patreon.config.max_attachment_bytes / (1024 * 1024))
    )


class AttachmentNotFound(ResourceMissing):
    def __init__(self, attachment_id):
        super().__init__('Attachment', attachment_id)


class AttachmentViewForbidden(ViewForbidden):
    def __init__(self, attachment_id):
        super().__init__('attachment_id', attachment_id)


class AttachmentEditForbidden(EditForbidden):
    def __init__(self, attachment_id):
        super().__init__('attachment_id', attachment_id)
