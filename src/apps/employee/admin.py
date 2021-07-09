from django.contrib import admin

from employee.models import Employee, Skill


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'unit', 'position', 'seniority', 'birth_date', )
    fields = ('first_name',
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
              'is_staff',
              'is_active',
              'skills',
              'unit'
              )


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Skill, SkillAdmin)
