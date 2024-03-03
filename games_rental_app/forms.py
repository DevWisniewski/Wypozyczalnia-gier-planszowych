from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser, Address

User = get_user_model()


class LoginForm(forms.Form):
    """
    Formularz logowania dla użytkowników.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        """
        Waliduje dane logowania.
        Sprawdza, czy użytkownik o podanej nazwie i haśle istnieje w systemie.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("Password and/or login is incorrect")
        else:
            self.user = user


class AddUserForm(forms.ModelForm):
    """
    Formularz do tworzenia nowego użytkownika.
    Sprawdza zgodność haseł i zapisuje użytkownika w systemie.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        """
        Sprawdza, czy oba hasła są identyczne.
        """
        pass1 = self.cleaned_data.get("password")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Passwords don't match")
        return pass2

    def save(self, commit=True):
        """
        Zapisuje użytkownika w systemie, ustawiając hasło.
        """
        user = super(AddUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class GameFilterForm(forms.Form):
    """
    Formularz służący do filtrowania gier planszowych.
    """

    # Wybór liczby graczy z opcją '---' na początku, oznaczającą brak wyboru.
    NUMBER_OF_PLAYERS_CHOICES = [(0, '---')] + [(i, str(i)) for i in range(1, 9)]
    number_of_players = forms.ChoiceField(choices=NUMBER_OF_PLAYERS_CHOICES, label='Liczba graczy', required=False)

    # Wybór minimalnego wieku gracza, dodano '+' przy liczbie.
    AGE_CHOICES = [(0, '---')] + [(i, f'{i}+') for i in range(2, 19)]
    min_age = forms.ChoiceField(choices=AGE_CHOICES, label='Minimalny wiek', required=False)

    # Wybór czasu trwania gry z zakresami czasu w minutach.
    DURATION_CHOICES = [(0, '---')] + [(i, f'{i} min') for i in [5, 10, 15, 30, 45, 60, 90, 120, 150, 180, 210, 240]]
    min_duration = forms.ChoiceField(choices=DURATION_CHOICES, label='Minimalny czas gry', required=False)
    max_duration = forms.ChoiceField(choices=DURATION_CHOICES, label='Maksymalny czas gry', required=False)

    # Wybór zakresu cenowego dla wypożyczenia gier, z etykietami określającymi ceny za dobę.
    PRICE_CHOICES = [(0, '---')] + [(i, f'{i} zł') for i in [2, 5, 10, 15, 20, 25, 30]]
    min_price = forms.ChoiceField(choices=PRICE_CHOICES, label='od', required=False)
    max_price = forms.ChoiceField(choices=PRICE_CHOICES, label='do', required=False)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'house_number', 'postal_code', 'city', 'country']
