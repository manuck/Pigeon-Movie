from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import MyUser
BIRTH_YEAR_CHOICES = [i for i in range(2019,1969,-1)]


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label='ID',widget=forms.TextInput(attrs={'placeholder':'3~15사이의 문자'}))
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
        label="생년월일",
        )
    class Meta:
        model = MyUser
        fields = ('username','password1','password2','date_of_birth')
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        us = MyUser.objects.all()
        if len(username) < 3 or len(username) > 15:
            raise forms.ValidationError("ID는 3글자이상15글자 이하로 해주세요.")
        
        for i in us:
            if username == i.username:
                raise forms.ValidationError("이미 존재하는 ID에요.")
        return username
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 맞지 않아요.")
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
    # password = ReadOnlyPasswordHashField()
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
        label="생년월일"
        )

    # favorite_genres = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=FAVORITE_GENRE,
    #     label="관심있는 장르 다중선택 가능"
    # )
    
    class Meta:
        model = MyUser
        fields = ('password1','password2','date_of_birth')

    # def clean_password(self):
    #     # Regardless of what the user provides, return the initial value.
    #     # This is done here, rather than on the field, because the
    #     # field does not have access to the initial value
    #     return self.initial["password"]

        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 맞지 않아요.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user





