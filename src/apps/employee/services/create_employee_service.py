from core.services import BaseService
from employee.models import Employee


class CreateEmployeeService(BaseService):
    def __init__(
            self,
            first_name,
            last_name,
            email,
            gender,
            employment_date,
            unit_id
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.employment_date = employment_date
        self.unit_id = unit_id

    def perform(self):
        self.instance = self._create_employee()

    def _create_employee(self):
        employee = Employee.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            gender=self.gender,
            employment_date=self.employment_date,
            unit_id=self.unit_id
        )
        return employee
