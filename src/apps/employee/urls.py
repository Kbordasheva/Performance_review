from django.urls import path

from employee.views import EmployeesListCreateView, EmployeeView

urlpatterns = [
    path('', EmployeesListCreateView.as_view(), name='employees'),
    path('<int:employee_id>/', EmployeeView.as_view(), name='employee'),
    ]
