from rest_framework import serializers

from core.serializers import DynamicFieldsSerializer
from employee.serializers import EmployeeSerializer


class CommentSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    author = EmployeeSerializer(
        fields=('id', 'full_name'),
        ref_name='CommentForEmployeeProfileSerializer',
        read_only=True,
    )
    text = serializers.CharField(max_length=1000)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class CriteriaSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=1000)
    is_done = serializers.BooleanField()
    start_date = serializers.DateField(allow_null=True)
    deadline = serializers.DateField(allow_null=True)
    finish_date = serializers.DateField(allow_null=True)


class GoalSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=1000)
    is_done = serializers.BooleanField()
    criteria = CriteriaSerializer(many=True)
    comments = CommentSerializer(many=True)


class PerformanceReviewSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    employee = EmployeeSerializer(
        fields=('id', 'full_name'),
        ref_name='PerformanceReviewForEmployeeProfileSerializer',
        read_only=True,
    )
    year = serializers.IntegerField(min_value=2000, max_value=2050)
    goals = GoalSerializer(many=True)


