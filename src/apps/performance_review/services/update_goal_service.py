from core.services import BaseService


class UpdateGoalService(BaseService):
    def __init__(self, instance, text, is_done):
        self.instance = instance
        self.text = text
        self.is_done = is_done

    def perform(self):
        self._save_goal()

    def _save_goal(self):
        self.instance.text = self.text
        self.instance.is_done = self.is_done

        self.instance.save()
