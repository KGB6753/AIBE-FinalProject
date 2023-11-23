from django.db import models
from users.models import User
from django.utils import timezone
# Create your models here.

class Food(models.Model):
    food_id = models.BigAutoField(primary_key=True)
    food_name = models.CharField(max_length=200)
    food_weight = models.DecimalField(max_digits=5,decimal_places=1)
    food_carbs = models.DecimalField(max_digits=5,decimal_places=1)
    food_proteins = models.DecimalField(max_digits=5,decimal_places=1)
    food_fats = models.DecimalField(max_digits=5,decimal_places=1)
    food_kcal = models.DecimalField(max_digits=5,decimal_places=1)

    class Meta:
        db_table = 'food'


class Photo(models.Model):
    photo_id = models.BigAutoField(primary_key=True)
    photo_url = models.ImageField(upload_to="images/", null=True, blank=True)

    class Meta:
        db_table = 'photo'
class Menu(models.Model):
    class category(models.TextChoices):
        OPTION1 = '1', '아침'
        OPTION2 = '2', '점심'
        OPTION3 = '3', '저녁'
        OPTION4 = '4', '간식'
        OPTION5 = '5', '야식'

    menu_id = models.BigAutoField(primary_key=True)
    menu_user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_food = models.ForeignKey(Food, on_delete=models.CASCADE)
    # menu_photo = models.ImageField(upload_to = "images/", null=True, blank=True)
    menu_photo = models.ForeignKey(Photo, on_delete=models.CASCADE,null=True, blank=True)
    menu_weight = models.DecimalField(max_digits=5,decimal_places=1)
    menu_date = models.DateTimeField()
    menu_category= models.CharField(max_length=20, choices=category.choices)

    def __str__(self):
        return str(self.title)
    class Meta:
        db_table = 'menu'

