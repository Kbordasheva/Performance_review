from core.services import BaseService


class  SaveEmployeeSkillsService(BaseService):
    def __init__(
            self,
            instance,
            skills,
    ) -> None:
        self.instance = instance
        self.skills = skills or list()

    def perform(self):
        self._save_skills()
        return True

    def _save_skills(self):
        self.instance.skills.set(self.skills, clear=True)

        self.instance.save()
