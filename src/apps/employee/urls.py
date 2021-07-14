from django.urls import path

from employee.views import EmployeesListCreateView, EmployeeView, SkillView, EmployeeSkillsUpdateView

urlpatterns = [
    path('', EmployeesListCreateView.as_view(), name='employees'),
    path('<int:employee_id>/', EmployeeView.as_view(), name='employee'),
    path('<int:employee_id>/skills/', EmployeeSkillsUpdateView.as_view(), name='employee-skills'),
    path('skills/', SkillView.as_view(), name='skills')
    ]
