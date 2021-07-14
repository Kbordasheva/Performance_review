from core.services import BaseService


class SaveEmployeeService(BaseService):
    def __init__(
            self,
            instance,
            first_name,
            first_name_ru,
            last_name,
            last_name_ru,
            middle_name_ru,
            gender,
            birth_date,
            email,
            phone,
            employment_date,
            dismiss_date,
            position,
            seniority,
            unit_id
    ):
        self.instance = instance
        self.first_name = first_name
        self.first_name_ru = first_name_ru
        self.last_name = last_name
        self.last_name_ru = last_name_ru
        self.middle_name_ru = middle_name_ru
        self.gender = gender
        self.birth_date = birth_date
        self.email = email
        self.phone = phone
        self.employment_date = employment_date
        self.dismiss_date = dismiss_date
        self.position = position
        self.seniority = seniority
        self.unit_id = unit_id

    def perform(self) -> bool:
        self._save_employee()
        return True

    def _save_employee(self):
        self.instance.first_name = self.first_name
        self.instance.first_name_ru = self.first_name_ru
        self.instance.last_name = self.last_name
        self.instance.last_name_ru = self.last_name_ru
        self.instance.middle_name_ru = self.middle_name_ru
        self.instance.gender = self.gender
        self.instance.birth_date = self.birth_date
        self.instance.email = self.email
        self.instance.phone = self.phone
        self.instance.employment_date = self.employment_date
        self.instance.dismiss_date = self.dismiss_date
        self.instance.position = self.position
        self.instance.seniority = self.seniority
        self.instance.unit_id = self.unit_id

        self.instance.save()
