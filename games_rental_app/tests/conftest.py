import pytest
from games_rental_app.models import CustomUser, Address, BoardGame, Inventory, Rental, ContactMessage

@pytest.fixture
def user(django_db_setup):
    # Tworzenie użytkownika
    user = CustomUser.objects.create_user(
        username="test_user",
        password="test_password",
        email="test_user@example.com",
    )
    return user


@pytest.fixture
def new_user_data():
    return {
        "username": "new_user",
        "password": "random_password123",
        "password2": "random_password123",
        "email": "new@example.com"
    }

@pytest.fixture
def sample_game(db):
    """Tworzy i zwraca przykładową grę do użycia w testach."""
    return BoardGame.objects.create(
        name="Testowa Gra",
        description="Opis Testowej Gry",
        number_of_players=[3, 4, 5],
        minimum_age=10,
        min_duration=30,
        max_duration=60,
        rental_price_per_day=10.00,
        category=['rodzinna', 'S', 'słowna', 'towarzyska'],
        image_name='Testowa_Gra.jpg'
    )


@pytest.fixture
def sample_address(db):
    """Tworzy i zwraca przykładowy adres do użycia w testach."""
    return Address.objects.create(
        street="Ulica",
        house_number="1",
        postal_code="00-123",
        city="Miasto",
        country="Kraj"
    )

@pytest.fixture
def staff_user(db):
    """
    Tworzy i zwraca użytkownika z uprawnieniami pracownika (is_staff=True).
    """
    return CustomUser.objects.create_user(
        username='staffuser',
        password='password',
        email='staff@example.com',
        is_staff=True
    )
