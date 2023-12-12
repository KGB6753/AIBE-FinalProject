from django.db import models
from users.models import User
from django.utils import timezone


# Create your models here.
class Diet(models.Model):
    class exercise(models.TextChoices):
        OPTION1 = '1', '매우 비활동적'
        OPTION2 = '2', '비활동적'
        OPTION3 = '3', '보통'
        OPTION4 = '4', '활동적'
        OPTION5 = '5', '매우 활동적'


    diet = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    diet_start_day = models.DateTimeField()
    diet_start_weight = models.DecimalField(max_digits=4, decimal_places=1)
    diet_target_weight = models.DecimalField(max_digits=4, decimal_places=1)
    diet_exercise = models.CharField(max_length=20, choices=exercise.choices)
    diet_user_height = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        db_table = 'diet'


class Weight(models.Model):
    weight_id = models.BigAutoField(primary_key=True)
    weight_current = models.DecimalField(max_digits=4, decimal_places=1)
    weight_recorded = models.DateTimeField()
    weight_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'weight'
