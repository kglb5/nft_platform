from patreon.exception import ResourceMissing


class PushInfoNotFound(ResourceMissing):
    def __init__(self, user_id, bundle_id, token):
        super().__init__('Push info', bundle_id)
        self.error_description = \
            "{} with token {} for user id {} and bundle id {} was not found." \
                .format('Push info', token, user_id, bundle_id)
