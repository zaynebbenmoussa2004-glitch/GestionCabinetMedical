from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone
# Create your models here.
def validate_past_date(value):
  if value >= timezone.localdate():
    raise ValidationError("la date de naissance doit etre anterieure a la date du jour")



class User(AbstractUser):
  pass



class Specialty(models.Model):
  name = models.CharField(max_length=100)

  class Meta:
    verbose_name = "Spécialité"
    verbose_name_plural = "Spécialités"

  def __str__(self):
    return self.name 



class Doctor(User):
  license_number=models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6)])
  phone=models.CharField(max_length=8, validators=[RegexValidator(regex=r"^\d{8}$" , message="le numero de telephone est non valide il doit contenir 8 chiffres")])
  specialties=models.ManyToManyField(Specialty, related_name="doctors")

  class Meta:
    verbose_name = "Médecin"
    verbose_name_plural = "Médecins"

  def __str__(self):
    return f"{self.first_name} {self.last_name}"



class Patient(User):
  national_id=models.CharField(max_length=8, unique=True, validators=[RegexValidator(regex=r"^\d{8}$" , message="le numero de CIN est non valide il doit contenir 8 chiffres")])
  phone=models.CharField(max_length=8, validators=[RegexValidator(regex=r"^\d{8}$" , message="le numero de telephone est non valide il doit contenir 8 chiffres")])
  birth_date=models.DateField(validators=[validate_past_date])

  class Meta:
    verbose_name = "Patient"
    verbose_name_plural = "Patients"

  def __str__(self):
    return f"{self.first_name} {self.last_name}"