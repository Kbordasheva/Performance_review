from rest_framework import serializers

from core.serializers import DynamicFieldsModelSerializer
from unit.models import Unit


class UnitSerializer(DynamicFieldsModelSerializer):
    manager = serializers.CharField(source='manager.full_name', read_only=True)

    class Meta:
        model = Unit
        fields = ('id', 'name', 'manager')
