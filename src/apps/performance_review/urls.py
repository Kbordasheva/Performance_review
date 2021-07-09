from django.urls import path

from performance_review.views import PerformanceReviewListCreateView

urlpatterns = [
    path('', PerformanceReviewListCreateView.as_view(), name='performance-review-all'),
    ]
