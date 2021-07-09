from django.urls import path

from employee.views import EmployeesListCreateView

urlpatterns = [
    path('', EmployeesListCreateView.as_view(), name='employees'),
    ]
