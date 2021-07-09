from django.shortcuts import render
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from employee.models import Employee
from employee.serializers import EmployeeSerializer


class BaseEmployeeView(GenericAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeesView(mixins.ListModelMixin, BaseEmployeeView):
    """ Get list of Employees.
    """

    ordering_fields = (
        ('id', 'id'),
        ('firstName', 'first_name'),
        ('lastName', 'last_name'),
    )
    ordering = ('id', )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
