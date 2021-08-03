from core.services import BaseService
from performance_review.models import PerformanceReview


class CreateReviewService(BaseService):
    def __init__(self, employee_id, year):
        self.employee_id = employee_id
        self.year = year

    def perform(self):
        self.instance = self._create_review()

        return True

    def _create_review(self):
        review = PerformanceReview.objects.create(
            employee_id=self.employee_id,
            year=self.year,
        )
        return review
