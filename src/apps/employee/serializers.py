from rest_framework import serializers

from core.serializers import DynamicFieldsSerializer, DynamicFieldsModelSerializer
from employee.choices import Gender, Seniority
from employee.models import Skill
from unit.serializers import UnitSerializer


class SkillSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class EmployeeListSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=200, allow_blank=True, write_only=True)
    last_name = serializers.CharField(max_length=200, allow_blank=True, write_only=True)
    full_name = serializers.CharField(read_only=True)
    unit = UnitSerializer()
    position = serializers.CharField(max_length=254, allow_blank=True)

    email = serializers.EmailField(max_length=200, allow_null=True)


class EmployeeSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    first_name = serializers.CharField(max_length=200, allow_blank=True)
    first_name_ru = serializers.CharField(max_length=200, allow_blank=True)
    last_name = serializers.CharField(max_length=200, allow_blank=True)
    last_name_ru = serializers.CharField(max_length=200, allow_blank=True)
    middle_name_ru = serializers.CharField(max_length=200, allow_blank=True)
    gender = serializers.ChoiceField(choices=Gender.choices, allow_null=True)
    birth_date = serializers.DateField(allow_null=True, read_only=True)
    email = serializers.EmailField(max_length=200, allow_null=True)
    phone = serializers.CharField(max_length=100, allow_blank=True)
    employment_date = serializers.DateField(allow_null=True)
    dismiss_date = serializers.DateField(allow_null=True)
    position = serializers.CharField(max_length=254, allow_blank=True)
    seniority = serializers.ChoiceField(choices=Seniority.choices, allow_null=True)
    skills = SkillSerializer(many=True)
    unit = UnitSerializer()
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

