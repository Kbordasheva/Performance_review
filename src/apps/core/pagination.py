from rest_framework.pagination import LimitOffsetPagination


class LimitedOffsetPagination(LimitOffsetPagination):
    max_limit = 100


class UnlimitedOffsetPagination(LimitOffsetPagination):
    max_limit = None
