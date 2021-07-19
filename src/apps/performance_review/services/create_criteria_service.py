from core.services import BaseService
from performance_review.models import Criteria


class CreateCriteriaService(BaseService):
    def __init__(
            self,
            goal_id,
            text,
            is_done,
            start_date,
            deadline,
            finish_date
    ):
        self.goal_id = goal_id
        self.text = text
        self.is_done = is_done
        self.start_date = start_date
        self.deadline = deadline
        self.finish_date = finish_date

    def perform(self):
        self.instance = self._save_criteria()

    def _save_criteria(self):
        criteria = Criteria.objects.create(
            goal_id=self.goal_id,
            text=self.text,
            is_done=self.is_done,
            start_date=self.start_date,
            deadline=self.deadline,
            finish_date=self.finish_date
        )
        return criteria
