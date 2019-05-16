from django import forms
from django.contrib import admin


from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import MyUser
BIRTH_YEAR_CHOICES = [i for i in range(2019,1969,-1)]
FAVORITE_GENRE = (('horror', '호러'),('action', '액션'),('comedy','코미디'),('docu','다큐'),)

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
        label="생년월일"
        )

    favorite_genres = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_GENRE,
        label="관심있는 장르 다중선택 가능"
    )
    
    
    class Meta:
        model = MyUser
        fields = ('username','' 'date_of_birth','favorite_genres')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

























































