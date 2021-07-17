from core.services import BaseService


class UpdateCommentService(BaseService):
    def __init__(
            self,
            instance,
            text
    ):
        self.instance = instance
        self.text = text

    def perform(self):
        self._save_comment()

        return True

    def _save_comment(self):
        self.instance.text = self.text

        self.instance.save()
