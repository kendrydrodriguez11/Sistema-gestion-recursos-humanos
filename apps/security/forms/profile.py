from django.forms import ModelForm
from apps.security.models import User

class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "dni",
            "email",
            "direction",
            "image",
        ]
    
