from core.services import BaseService


class MarkGoalDoneService(BaseService):
    def __init__(self, instance, is_done):
        self.instance = instance
        self.is_done = is_done

    def perform(self):
        self._save_goal()

    def _save_goal(self):
        self.instance.is_done = self.is_done

        self.instance.save()
