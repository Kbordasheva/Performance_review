from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from performance_review.models import PerformanceReview
from performance_review.serializers import PerformanceReviewSerializer, PerformanceReviewDetailsSerializer


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
