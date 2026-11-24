from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.



class Appointment(models.Model):

  class Status(models.TextChoices):
    PENDING = "PENDING", "En attente"
    CONFIRMED = "CONFIRMED", "Confirmé"
    CANCELLED = "CANCELLED", "Annulé"

  reason=models.TextField()
  prescription=models.FileField(upload_to="prescriptions/", blank=True, validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
  status=models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
  duration_minutes=models.PositiveIntegerField(default=30)
  appointment_date=models.DateTimeField()
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  doctor=models.ForeignKey("AccountApp.Doctor", on_delete=models.CASCADE, related_name="appointments")
  patient=models.ForeignKey("AccountApp.Patient", on_delete=models.CASCADE, related_name="appointments")

  class Meta:
    ordering = ["appointment_date"]
    constraints = [
      models.UniqueConstraint(fields=["doctor", "appointment_date"], name="unique_doctor_appointment_date")
    ]

  def clean(self):
    super().clean()
    if self.appointment_date is None:
      return
    date_changed = True
    if self.pk:
      old_date = Appointment.objects.filter(pk=self.pk).values_list("appointment_date", flat=True).first()
      date_changed = old_date != self.appointment_date
    if date_changed and self.appointment_date <= timezone.now():
      raise ValidationError({"appointment_date": "la date du rendez-vous doit etre posterieure a la date actuelle"})

  def __str__(self):
    return f"{self.patient} - {self.doctor} - {self.appointment_date}"