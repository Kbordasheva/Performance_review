from django.urls import path

from employee.views import EmployeesListCreateView, EmployeeView, SkillView, EmployeeSkillsUpdateView, EmployeeProfile

urlpatterns = [
    path('', EmployeesListCreateView.as_view(), name='employees'),
    path('<int:employee_id>/', EmployeeView.as_view(), name='employee'),
    path('<int:employee_id>/skills/', EmployeeSkillsUpdateView.as_view(), name='employee-skills'),
    path('profile/<int:employee_id>/', EmployeeProfile.as_view(), name='employee-profile'),
    path('skills/', SkillView.as_view(), name='skills')
    ]
