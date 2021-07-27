import logging

from rest_framework import mixins, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import ServiceException
from core.pagination import UnlimitedOffsetPagination
from core.permissions import IsManagerOrReadOnly
from employee.models import Employee, Skill
from employee.serializers import (
    EmployeeSerializer,
    EmployeeListSerializer,
    SkillSerializer,
    SkillsUpdateSerializer,
)
from employee.services.create_employee_service import CreateEmployeeService
from employee.services.save_employee_skills_service import SaveEmployeeSkillsService
from employee.services.update_employee_service import SaveEmployeeService
from performance_review.serializers import EmployeeProfileSerializer
from unit.models import Unit

logger = logging.getLogger('project')


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'employee': {
                'id': user.pk,
                'name': user.full_name,
                'email': user.email
            }
        })


class LogoutView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = None

    def post(self, request):
        if request.user.is_authenticated:
            request.auth.delete()

        return Response()


class EmployeesListCreateView(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              GenericAPIView):
    permission_classes = (
        IsManagerOrReadOnly,
    )
    serializer_class = EmployeeListSerializer

    def get_queryset(self):
        queryset = Employee.objects.select_related('unit')\
            .filter(is_superuser=False, is_active=True)  # don't show superuser acc
        if not self.request.user.is_manager and not self.request.user.is_staff:
            # The employee can only see their profiles.
            queryset = Employee.objects.filter(id=self.request.user.id)

        elif self.request.user.is_manager:  # managers can see only their units employees
            unit = Unit.objects.get(manager=self.request.user)
            queryset = Employee.objects.filter(unit=unit)

        return queryset

    ordering_fields = (
        ('id', 'id'),
        ('firstName', 'first_name'),
        ('lastName', 'last_name'),
    )
    ordering = ('id',)

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
                'gender',
                'employment_date',
                'unit_id'
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


class EmployeeView(GenericAPIView, mixins.RetrieveModelMixin):
    permission_classes = (
        IsManagerOrReadOnly,
    )
    lookup_url_kwarg = 'employee_id'
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = Employee.objects \
            .select_related('unit').prefetch_related('skills')

        if not self.request.user.is_manager and not self.request.user.is_staff:
            # The employee can only see their profiles.
            queryset = Employee.objects.filter(id=self.request.user.id)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            logger.error(
                f'Validation error on Employee profile update. '
                f'Reason: {serializer.errors}'
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        employee_data = {}
        for key in (
                'first_name',
                'first_name_ru',
                'last_name',
                'last_name_ru',
                'middle_name_ru',
                'gender',
                'birth_date',
                'email',
                'phone',
                'employment_date',
                'dismiss_date',
                'position',
                'seniority',
                'unit_id'):
            employee_data[key] = serializer.validated_data.get(key, getattr(instance, key))

        service = SaveEmployeeService(instance, **employee_data)
        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot save details for employee ID {instance.id}. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service.instance)
        return Response(serializer.data)


class SkillView(ListCreateAPIView):
    pagination_class = UnlimitedOffsetPagination
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()

    ordering_fields = (
        ('id', 'id'),
    )
    ordering = ('id',)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EmployeeSkillsUpdateView(mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = SkillsUpdateSerializer
    lookup_url_kwarg = 'employee_id'
    queryset = Employee.objects.all()

    def put(self, request, *args, **kwargs):
        """
        Add skills by IDs to the Employee.
        """
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            logger.error(
                f'Validation error on Employee Skills update. '
                f'Reason: {serializer.errors}'
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = SaveEmployeeSkillsService(
            instance=instance,
            **serializer.validated_data,
        )
        try:
            service.perform()
        except ServiceException as e:
            logger.error(f'Cannot update skills for Employee ID {instance.id}. Reason: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(service.skills)


class EmployeeProfile(mixins.RetrieveModelMixin, GenericAPIView):
    serializer_class = EmployeeProfileSerializer
    lookup_url_kwarg = 'employee_id'

    def get_queryset(self):
        queryset = Employee.objects.select_related('unit').prefetch_related('skills')

        if not self.request.user.is_manager and not self.request.user.is_staff:
            # The employee can only see their profiles.
            queryset = Employee.objects.filter(id=self.request.user.id)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
