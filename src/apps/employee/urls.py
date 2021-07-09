from django.urls import path

from employee.views import EmployeesView

urlpatterns = [
    path('', EmployeesView.as_view(), name='employees'),
    ]