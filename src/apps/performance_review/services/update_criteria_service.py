from core.services import BaseService


class UpdateCriteriaService(BaseService):
    def __init__(
            self,
            instance,
            text,
            is_done,
            start_date,
            deadline,
            finish_date
    ):
        self.instance = instance
        self.text = text
        self.is_done = is_done
        self.start_date = start_date
        self.deadline = deadline
        self.finish_date = finish_date

    def perform(self):
        self._save_criteria()

        return True

    def _save_criteria(self):
        self.instance.text = self.text
        self.instance.is_done = self.is_done
        self.instance.start_date = self.start_date
        self.instance.deadline = self.deadline
        self.instance.finish_date = self.finish_date

        self.instance.save()
