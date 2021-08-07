from django.urls import path

from performance_review.views import (
    PerformanceReviewListCreateView,
    PerformanceReviewDetailsView,
    GoalCreateView,
    GoalUpdateView,
    CommentCreateView,
    CommentUpdateView,
    CriteriaCreateView,
    CriteriaUpdateView,
    GoalDeleteView,
)

urlpatterns = [
    path('', PerformanceReviewListCreateView.as_view(), name='performance-review-all'),
    path('<int:profile_id>/', PerformanceReviewDetailsView.as_view(), name='performance-review-details'),
    path('<int:profile_id>/goals/', GoalCreateView.as_view(), name='goals'),
    path('<int:profile_id>/goals/<int:goal_id>/',
         GoalUpdateView.as_view(),
         name='goal'),
    path('<int:profile_id>/goals/<int:goal_id>/delete/',
         GoalDeleteView.as_view(), name='delete-goal'),
    path('<int:profile_id>/goals/<int:goal_id>/comments/',
         CommentCreateView.as_view(),
         name='comments'),
    path('<int:profile_id>/goals/<int:goal_id>/comments/<int:comment_id>/',
         CommentUpdateView.as_view(),
         name='comment'),
    path('<int:profile_id>/goals/<int:goal_id>/criteria/',
         CriteriaCreateView.as_view(),
         name='criteria-all'),
    path('<int:profile_id>/goals/<int:goal_id>/criteria/<int:criteria_id>/',
         CriteriaUpdateView.as_view(),
         name='criteria'),
    ]
