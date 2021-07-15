from rest_framework import serializers

from core.serializers import DynamicFieldsSerializer, DynamicFieldsModelSerializer
from employee.choices import Gender, Seniority
from employee.models import Skill
from unit.serializers import UnitSerializer


class SkillSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class SkillsUpdateSerializer(DynamicFieldsSerializer):
    skills = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        max_length=100,
        allow_empty=True,
        default=list,
        write_only=True
    )


class EmployeeListSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=200, allow_blank=True, write_only=True)
    last_name = serializers.CharField(max_length=200, allow_blank=True, write_only=True)
    full_name = serializers.CharField(read_only=True)
    unit = UnitSerializer()
    position = serializers.CharField(max_length=254, allow_blank=True)
    seniority = serializers.ChoiceField(choices=Seniority.choices, allow_null=True)
    skills = SkillSerializer(many=True)
    email = serializers.EmailField(max_length=200, allow_null=True)
    goals_count = serializers.SerializerMethodField()
    goals_done_count = serializers.SerializerMethodField()

    def get_goals_count(self, employee):
        if employee.current_review:
            return employee.current_review.goals.count()
        return ''

    def get_goals_done_count(self, employee):
        if employee.current_review:
            return employee.current_review.goals.filter(is_done=True).count()
        return ''


class EmployeeSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(read_only=True, required=False)
    full_name_ru = serializers.CharField(read_only=True, required=False)
    first_name = serializers.CharField(max_length=200, allow_blank=True, required=False)
    first_name_ru = serializers.CharField(max_length=200, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=200, allow_blank=True, required=False)
    last_name_ru = serializers.CharField(max_length=200, allow_blank=True, required=False)
    middle_name_ru = serializers.CharField(max_length=200, allow_blank=True, required=False)
    gender = serializers.ChoiceField(choices=Gender.choices, allow_null=True, required=False)
    birth_date = serializers.DateField(allow_null=True, read_only=True, required=False)
    email = serializers.EmailField(max_length=200, allow_null=True, required=False)
    phone = serializers.CharField(max_length=100, allow_blank=True, required=False)
    employment_date = serializers.DateField(allow_null=True, required=False)
    dismiss_date = serializers.DateField(allow_null=True, required=False)
    position = serializers.CharField(max_length=254, allow_blank=True, required=False)
    seniority = serializers.ChoiceField(choices=Seniority.choices, allow_null=True, required=False)
    skills = SkillSerializer(many=True, required=False)
    unit = UnitSerializer(required=False, read_only=True)
    unit_id = serializers.IntegerField(write_only=True, required=False)
    is_staff = serializers.BooleanField(read_only=True, required=False)
    is_active = serializers.BooleanField(read_only=True, required=False)
