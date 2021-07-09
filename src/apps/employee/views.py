import logging

from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.exceptions import ServiceException
from employee.models import Employee
from employee.serializers import EmployeeSerializer, EmployeeListSerializer
from employee.services.create_employee_service import CreateEmployeeService

logger = logging.getLogger('project')


class BaseEmployeeView(GenericAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeesListCreateView(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              BaseEmployeeView):
    serializer_class = EmployeeListSerializer

    ordering_fields = (
        ('id', 'id'),
        ('firstName', 'first_name'),
        ('lastName', 'last_name'),
    )
    ordering = ('id', )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create a new employee.
        """
        serializer = self.get_serializer(
            data=request.data,
            ref_name='EmployeeCreateSerializer',
            fields=(
                'first_name',
                'last_name',
                'email',
            ),
        )
        if not serializer.is_valid():
            logger.error(
                f'Validation error on a new employee creation. '
                f'Reason: {serializer.errors}'
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = CreateEmployeeService(**serializer.validated_data)

        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot create relocation request. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
