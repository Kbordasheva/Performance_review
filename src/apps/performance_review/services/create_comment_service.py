from core.services import BaseService
from performance_review.models import Comment


class CreateCommentService(BaseService):
    def __init__(
            self,
            goal_id,
            author,
            text,
    ):
        self.goal_id = goal_id
        self.author = author
        self.text = text

    def perform(self):
        self.instance = self._create_comment()

        return True

    def _create_comment(self):
        comment = Comment.objects.create(
            goal_id=self.goal_id,
            author=self.author,
            text=self.text,
        )
        return comment
