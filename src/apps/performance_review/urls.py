from django.urls import path

from performance_review.views import PerformanceReviewListCreateView, PerformanceReviewDetailsView

urlpatterns = [
    path('', PerformanceReviewListCreateView.as_view(), name='performance-review-all'),
    path('<int:profile_id>/', PerformanceReviewDetailsView.as_view(), name='performance-review-details')
    ]
