from core.services import BaseService
from employee.models import Employee


class CreateEmployeeService(BaseService):
    def __init__(
            self,
            first_name,
            last_name,
            email
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def perform(self):
        self.instance = self._create_employee()

    def _create_employee(self):
        employee = Employee.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email
        )
        return employee
