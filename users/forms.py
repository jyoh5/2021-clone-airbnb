from django import forms
from . import models


class LoginForm(forms.Form):

    """LoginForm Definition"""

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong."))
                # raise forms.ValidationError("Password is wrong.")
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist."))
            # raise forms.ValidationError("User does not exist.")

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User does not exist.")

    # def clean_password(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password(password):
    #             return password
    #         else:
    #             raise forms.ValidationError("Password is wrong.")
    #     except models.User.DoesNotExist:
    #         pass


class SignUpForm(forms.ModelForm):

    """SignUpForm Definition"""

    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email"]

    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(email=email)
    #         raise forms.ValidationError("Email already exists.")
    #     except models.User.DoesNotExist:
    #         return email

    def clean_password_check(self):
        password = self.cleaned_data.get("password")
        password_check = self.cleaned_data.get("password_check")

        if password == password_check:
            return password
        else:
            raise forms.ValidationError("Password does not match.")

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = super().save(commit=False)
        user.username = email
        user.set_password(password)
        user.save()

    # 방법 1
    # class SignUpForm(forms.Form):
    # first_name = forms.CharField(max_length=80)
    # last_name = forms.CharField(max_length=80)
    # email = forms.EmailField()
    # password = forms.CharField(widget=forms.PasswordInput)
    # password_check = forms.CharField(
    #     widget=forms.PasswordInput, label="Confirm Password"
    # )

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(email=email)
    #         raise forms.ValidationError("Email already exists.")
    #     except models.User.DoesNotExist:
    #         return email

    # def clean_password_check(self):
    #     password = self.cleaned_data.get("password")
    #     password_check = self.cleaned_data.get("password_check")

    #     if password == password_check:
    #         return password
    #     else:
    #         raise forms.ValidationError("Password does not match.")

    # def save(self):
    #     first_name = self.cleaned_data.get("first_name")
    #     last_name = self.cleaned_data.get("last_name")
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")

    #     user = models.User.objects.create_user(email, email, password)
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.save()
