from django import forms
from .models import User, Diet, Weight
from django.utils import timezone
from django.shortcuts import get_object_or_404


class GoalForm(forms.ModelForm):
    class Meta:
        model = Diet
        fields = ['diet', 'diet_start_weight', 'diet_target_weight', 'diet_exercise', 'diet_user_height']

    def save(self, commit=True):
        diet = self.cleaned_data['diet']
        diet_start_weight = self.cleaned_data['diet_start_weight']
        diet_target_weight = self.cleaned_data['diet_target_weight']
        diet_exercise = self.cleaned_data['diet_exercise']
        diet_user_height = self.cleaned_data['diet_user_height']

        try:
            # Attempt to get an existing Diet object
            instance_of_diet = Diet.objects.get(diet=diet)
            instance_of_diet.diet_start_day = timezone.now()
            instance_of_diet.diet_start_weight = diet_start_weight
            instance_of_diet.diet_target_weight = diet_target_weight
            instance_of_diet.diet_exercise = diet_exercise
            instance_of_diet.diet_user_height = diet_user_height


        except Diet.DoesNotExist:
            # Create a new Diet object if it doesn't exist
            instance_of_diet = Diet.objects.create(
                diet=diet,
                diet_start_day=timezone.now(),
                diet_start_weight=diet_start_weight,
                diet_target_weight=diet_target_weight,
                diet_exercise=diet_exercise,
                diet_user_height=diet_user_height
            )
        Weight.objects.create(
            weight_user=diet,
            weight_current=diet_start_weight,
            weight_recorded=timezone.now()
        )

        instance_of_diet.save()


class BodyForm(forms.ModelForm):
    weight_current = forms.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        model = Diet
        fields = ['diet_exercise', 'diet_user_height']
