from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm


User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@example.com',
            'autocomplete': 'email',
        }),
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور',
            'autocomplete': 'current-password',
        }),
    )

    error_messages = {
        'invalid_login': 'ایمیل یا رمز عبور درست نیست.',
        'inactive': 'این حساب غیرفعال است.',
    }

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                user = None

            username = user.get_username() if user else email
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='نام',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'نام شما',
            'autocomplete': 'given-name',
        }),
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@example.com',
            'autocomplete': 'email',
        }),
    )
    password1 = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور',
            'autocomplete': 'new-password',
        }),
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'تکرار رمز عبور',
            'autocomplete': 'new-password',
        }),
    )

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('با این ایمیل قبلا حساب ساخته شده است.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name'].strip()
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AccountPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='رمز عبور فعلی',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور فعلی',
            'autocomplete': 'current-password',
        }),
    )
    new_password1 = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور جدید',
            'autocomplete': 'new-password',
        }),
    )
    new_password2 = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'تکرار رمز عبور جدید',
            'autocomplete': 'new-password',
        }),
    )
