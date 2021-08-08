import logging

from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView, CreateAPIView, get_object_or_404
from rest_framework.response import Response

from core.exceptions import ServiceException
from performance_review.models import PerformanceReview, Goal, Comment, Criteria
from performance_review.serializers import (
    PerformanceReviewSerializer,
    PerformanceReviewDetailsSerializer,
    GoalSerializer,
    CommentSerializer,
    CriteriaSerializer,
    PerformanceReviewCreateSerializer, GoalMarkDoneSerializer,
)
from performance_review.services.create_comment_service import CreateCommentService
from performance_review.services.create_criteria_service import CreateCriteriaService
from performance_review.services.create_goal_service import CreateGoalService
from performance_review.services.create_review_service import CreateReviewService
from performance_review.services.mark_goal_done_service import MarkGoalDoneService
from performance_review.services.update_comment_service import UpdateCommentService
from performance_review.services.update_criteria_service import UpdateCriteriaService
from performance_review.services.update_goal_service import UpdateGoalService

logger = logging.getLogger('project')


class PerformanceReviewListCreateView(mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      GenericAPIView
                                      ):
    serializer_class = PerformanceReviewSerializer

    def get_queryset(self):
        queryset = PerformanceReview.objects \
            .select_related(
            'employee',
        )

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer_fields = (
            'id',
            'employee',
            'year',
            'goals_count',
            'goals_done_count'
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, fields=serializer_fields, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, fields=serializer_fields, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PerformanceReviewCreateSerializer(data=request.data)

        if not serializer.is_valid():
            logger.error(
                f'Validation error on Performance review create. '
                f'Reason: {serializer.errors}'
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = CreateReviewService(**serializer.validated_data)

        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot create Performance review. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service.instance)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "id": service.instance.id,
            "year": service.instance.year,
            "goals": []
        },
            status=status.HTTP_201_CREATED, headers=headers)


class PerformanceReviewDetailsView(mixins.RetrieveModelMixin, GenericAPIView):
    serializer_class = PerformanceReviewDetailsSerializer
    lookup_url_kwarg = 'profile_id'

    def get_queryset(self):
        queryset = PerformanceReview.objects \
            .select_related(
            'employee',
            'employee__unit',
        )

        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GoalCreateView(CreateAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def get_queryset(self):
        queryset = PerformanceReview.objects.select_related('employee')

        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        queryset = self.get_queryset()
        review = get_object_or_404(queryset, id=self.kwargs['profile_id'])

        if not serializer.is_valid():
            logger.error(
                f'Validation error on Goal create. '
                f'Reason: {serializer.errors}'
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = CreateGoalService(review_id=review.id,
                                    **serializer.validated_data)

        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot create Goal for review ID {review.id}. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GoalUpdateView(mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
    lookup_url_kwarg = 'goal_id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            logger.error(
                f'Validation error on Goal ID {instance.id} update. '
                f'Reason: {serializer.errors}'

            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = UpdateGoalService(instance, **serializer.validated_data)

        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot save Goal. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service.instance)
        return Response(serializer.data)


class MarkGoalDoneView(mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = GoalMarkDoneSerializer
    queryset = Goal.objects.all()
    lookup_url_kwarg = 'goal_id'

    def put(self, request, *args, **kwargs):
        """Only a manager can mark a goal as done."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            logger.error(
                f'Validation error on Goal ID {instance.id} mark as done. '
                f'Reason: {serializer.errors}'

            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = MarkGoalDoneService(instance, **serializer.validated_data)

        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot mark Goal as done. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service.instance)
        return Response(serializer.data)


class GoalDeleteView(mixins.DestroyModelMixin, GenericAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def get_goal(self):
        goal = get_object_or_404(
            Goal.objects.filter(id=self.kwargs['goal_id'])
        )
        return goal

    def delete(self, request, *args, **kwargs):
        """ Delete Goal by its Id.
        """
        goal = self.get_goal()
        goal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.select_related('author', )

    def get_queryset(self):
        queryset = Goal.objects.select_related('review')

        return queryset

    def post(self, request, *args, **kwargs):
        """
        Create a new comment.
        """
        serializer = self.get_serializer(data=request.data)
        queryset = self.get_queryset()
        goal = get_object_or_404(queryset, id=self.kwargs['goal_id'])

        if not serializer.is_valid():
            logger.error(
                f'Validation error on comment save. '
                f'Reason: {serializer.errors}'
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = CreateCommentService(
            goal_id=goal.id,
            author=request.user,
            **serializer.validated_data,
        )
        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot save comment. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentUpdateView(mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'comment_id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            logger.error(
                f'Validation error on Comment ID {instance.id} update. '
                f'Reason: {serializer.errors}'
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = UpdateCommentService(instance, **serializer.validated_data)
        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot save Comment ID {instance.id}. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service.instance)
        return Response(serializer.data)


class CriteriaCreateView(CreateAPIView):
    serializer_class = CriteriaSerializer
    queryset = Criteria.objects.select_related('goal', )

    def get_queryset(self):
        queryset = Goal.objects.select_related('review')

        return queryset

    def post(self, request, *args, **kwargs):
        """
        Create a new criteria.
        """
        serializer = self.get_serializer(data=request.data)
        queryset = self.get_queryset()
        goal = get_object_or_404(queryset, id=self.kwargs['goal_id'])

        if not serializer.is_valid():
            logger.error(
                f'Validation error on criteria save. '
                f'Reason: {serializer.errors}'
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = CreateCriteriaService(
            goal_id=goal.id,
            **serializer.validated_data,
        )
        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot save criteria. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CriteriaUpdateView(mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = CriteriaSerializer
    queryset = Criteria.objects.all()
    lookup_url_kwarg = 'criteria_id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            logger.error(
                f'Validation error on Criteria ID {instance.id} update. '
                f'Reason: {serializer.errors}'
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = UpdateCriteriaService(instance, **serializer.validated_data)
        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot save Criteria ID {instance.id}. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service.instance)
        return Response(serializer.data)
