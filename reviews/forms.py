from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    review = forms.CharField(max_length=80, min_length=10)

    class Meta:
        model = models.Review
        fields = ("review",
                  "accuracy",
                  "communication",
                  "cleanliness",
                  "location",
                  "check_in",
                  "value",
                  )

    def save(self):
        review = super().save(commit=False)
        return review
