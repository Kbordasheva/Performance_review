from django.db.models import IntegerChoices, TextChoices


class Gender(IntegerChoices):
    MALE = 1, 'Male'
    FEMALE = 2, 'Female'


class Seniority(TextChoices):
    BEGINNER = 'beginner', 'Beginner'
    JUNIOR = 'junior', 'Junior'
    MIDDLE = 'middle', 'Middle'
    SENIOR = 'senior', 'Senior'
