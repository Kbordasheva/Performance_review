from core.services import BaseService
from performance_review.models import Goal


class CreateGoalService(BaseService):
    def __init__(
            self,
            review_id,
            text,
    ):
        self.review_id = review_id
        self.text = text

    def perform(self):
        self.instance = self._create_goal()

        return True

    def _create_goal(self):
        goal = Goal.objects.create(
            review_id=self.review_id,
            text=self.text,
        )
        return goal
