from django.db.models import IntegerChoices, TextChoices


class Gender(IntegerChoices):
    MALE = 1, 'Male'
    FEMALE = 2, 'Female'


class Seniority(TextChoices):
    BEGINNER = 'beginner', 'Beginner'
    JUNIOR = 'junior', 'Junior'
    MIDDLE = 'middle', 'Middle'
    SENIOR = 'senior', 'Senior'


class EmployeeRole(TextChoices):
    EMPLOYEE = 'employee', 'Employee'
    ROLES_MASTER = 'roles_master', 'Roles Master'
    MANAGER = 'manager', 'Manager'

    @classmethod
    def manager_roles(cls) -> tuple:
        return (
            cls.MANAGER.value,
        )
