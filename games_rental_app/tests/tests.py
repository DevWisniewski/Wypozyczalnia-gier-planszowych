from django.urls import reverse
import pytest
from django.test import Client
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from games_rental_app.models import CustomUser, BoardGame, BoardGame, Address, Inventory, Rental, ContactMessage


# **************************************************
# Testy dla widoku ContactView
# **************************************************
@pytest.mark.django_db
def test_contact_view(client):
    """
    Sprawdza, czy:
    - widok zwraca status HTTP 200, co wskazuje na poprawne ładowanie strony,
    - strona zawiera frazę 'Kontakt', co potwierdza wyświetlenie odpowiedniej treści,
    - strona zawiera kluczowe elementy formularza kontaktowego, w tym pola 'Imię', 'Email' i 'Wiadomość'.
    """
    url = reverse('contact')
    response = client.get(url)
    content = response.content.decode('utf-8')

    assert response.status_code == 200
    assert 'Kontakt' in content
    assert 'name="name"' in content  # Sprawdza obecność pola "Imię"
    assert 'name="email"' in content  # Sprawdza obecność pola "Email"
    assert 'name="message"' in content  # Sprawdza obecność pola "Wiadomość"


# **************************************************
# Testy dla widoku WelcomeView
# **************************************************
@pytest.mark.django_db
def test_welcome_view(client):
    """
    Sprawdza, czy:
        - widok zwraca status HTTP 200, co wskazuje na poprawne ładowanie strony,
        - strona zawiera frazę 'Naszą Wypożyczalnią!', co potwierdza wyświetlenie odpowiedniej treści.
    """
    url = reverse('welcome')
    response = client.get(url)
    content = response.content.decode('utf-8')  # Dekodowanie zawartości odpowiedzi

    assert response.status_code == 200
    assert 'Naszą Wypożyczalnią!' in content


# **************************************************
# Testy dla widoku Login i AddUser
# **************************************************
@pytest.mark.django_db
def test_login(client, user):
    """
    Test logowania użytkownika.

    Sprawdza, czy:
        - po wprowadzeniu prawidłowych danych logowania, użytkownik jest przekierowywany (status HTTP 302),
        - przekierowanie kieruje na oczekiwaną stronę 'my_account'.
    Używa danych użytkownika, zdefiniowanych w fixture `user`.
    """
    username = user.username
    password = "test_password"  # hasło, które zostało użyte w fixture `user` do stworzenia użytkownika

    url = reverse('login')
    response = client.post(url, {'username': username, 'password': password})
    assert response.status_code == 302, "Oczekiwane przekierowanie po zalogowaniu"
    assert response.url == reverse('my_account'), "Przekierowanie powinno kierować na stronę 'my_account'"


@pytest.mark.django_db
def test_add_user_view_submission(client, new_user_data):
    """
    Test dla widoku AddUserView sprawdzający funkcjonalność formularza dodawania użytkownika.
    Sprawdza, czy:
        - formularz po wypełnieniu i wysłaniu przekierowuje na stronę logowania,
        - czy nowy użytkownik zostaje poprawnie utworzony w bazie danych.
    Używa danych użytkownika, zdefiniowanych w fixture `new_user_data`.
    """
    url = reverse('add_user')
    response = client.post(url, new_user_data)
    content = response.content.decode('utf-8')
    assert 'error' not in content, "Formularz zawiera błędy walidacji"

    assert response.status_code == 302  # Sprawdzenie, czy następuje przekierowanie
    assert response.url == reverse('login')  # Sprawdzenie, czy przekierowanie kieruje na stronę logowania

    # Sprawdzamy, czy użytkownik został utworzony
    assert CustomUser.objects.filter(username=new_user_data['username']).exists()


# **************************************************
# Testy dla szablonu base.html, po którym dziedziczą inne szablony aplikacji
# **************************************************
@pytest.mark.django_db
def test_base_template_elements(client):
    """
    Test sprawdzający obecność kluczowych elementów w szablonie base.html.
    """
    url = reverse('welcome')  # wprowadzamy widok który, dziedziczy po base
    response = client.get(url)
    content = response.content.decode('utf-8')

    # Sprawdzenie obecności elementów zdefiniowanych szablonie w base.html
    assert '632762475' in content  # Przykładowy numer telefonu
    assert 'wypozyczalniagier@gmail.com' in content  # Przykładowy email
    assert 'ul. Świętego Mikołaja 7, 25-477 Gorzów Wielkopolski' in content  # Przykładowy adres

    # Sprawdzenie obecności linków w pasku nawigacyjnym
    assert reverse('welcome') in content
    assert reverse('game_list') in content
    assert reverse('contact') in content


@pytest.mark.django_db
def test_base_template_navigation_links(client):
    """
    Test sprawdza, czy linki w pasku nawigacyjnym prowadzą do odpowiednich stron.
    """
    url = reverse('login')  # wprowadzamy widok który, dziedziczy po base
    response = client.get(url)
    content = response.content.decode('utf-8')

    # Sprawdzenie obecności linków nawigacyjnych
    assert 'href="' + reverse('welcome') + '"' in content
    assert 'href="' + reverse('game_list') + '"' in content
    assert 'href="' + reverse('contact') + '"' in content


@pytest.mark.django_db
def test_base_template_auth_dependent_elements(client, user):
    """
    Test sprawdza, czy elementy zależne od stanu uwierzytelnienia użytkownika są odpowiednio wyświetlane.
    """
    url = reverse('login')  # wprowadzamy widok który, dziedziczy po base

    # Test dla niezalogowanego użytkownika
    response = client.get(url)
    content = response.content.decode('utf-8')
    assert 'Utwórz konto' in content
    assert 'Zaloguj' in content

    # Test dla zalogowanego użytkownika
    client.force_login(user)
    response = client.get(url)
    content = response.content.decode('utf-8')
    assert 'Moje konto' in content
    assert 'Wyloguj' in content


# **************************************************
# Testy dla widoku GameDetailsView
# **************************************************
@pytest.mark.django_db
def test_game_details_view(client, sample_game):
    """
    Test dla widoku GameDetailsView.

    Sprawdza, czy:
        - widok szczegółów gry zwraca status HTTP 200, co wskazuje na poprawne ładowanie strony,
        - na stronie znajdują się kluczowe informacje o grze, takie jak jej nazwa i opis,
          co potwierdza, że odpowiednie dane są wyświetlane na stronie.

    Fixture 'sample_game' jest używana do stworzenia przykładowej gry, co pozwala na testowanie
    widoku szczegółów gry z rzeczywistymi danymi.
    """
    url = reverse('dynamic_game_detail', kwargs={'slug': sample_game.slug})
    response = client.get(url)
    content = response.content.decode('utf-8')

    assert response.status_code == 200
    assert sample_game.name in content
    assert sample_game.description in content


@pytest.mark.django_db
def test_game_availability(client, sample_game):
    """
    Test sprawdzający dostępność gry w GameDetailsView.

    Sprawdza, czy na stronie szczegółów gry wyświetlana jest informacja o jej dostępności:
        - 'Na stanie', jeśli istnieją niewypożyczone egzemplarze gry,
        - 'Brak w magazynie', jeśli nie ma dostępnych egzemplarzy.
    """
    # Dodanie egzemplarza gry do magazynu
    Inventory.objects.create(game=sample_game, is_rented=False)

    url = reverse('dynamic_game_detail', kwargs={'slug': sample_game.slug})
    response = client.get(url)
    content = response.content.decode('utf-8')

    assert 'Na stanie' in content or 'Brak w magazynie' in content


@pytest.mark.django_db
def test_game_rental(client, sample_game, user):
    """
    Test sprawdzający funkcjonalność wypożyczenia gry.

    Sprawdza, czy:
        - po wysłaniu żądania POST na widok szczegółów gry z odpowiednimi danymi,
          następuje przekierowanie (co sugeruje udane wypożyczenie),
        - wypożyczenie gry jest faktycznie tworzone w bazie danych.
    """
    # Dodanie egzemplarza gry do magazynu
    inventory_item = Inventory.objects.create(game=sample_game, is_rented=False)

    # Zalogowanie użytkownika
    client.login(username=user.username, password='test_password')

    url = reverse('dynamic_game_detail', kwargs={'slug': sample_game.slug})
    response = client.post(url, {'rent_game': 'true'})

    assert response.status_code == 302  # Sprawdzenie przekierowania
    # Sprawdzenie, czy wypożyczenie zostało utworzone
    assert Rental.objects.filter(user=user, inventory=inventory_item).exists()


# **************************************************
# Testy dla widoku GameListView
# **************************************************
@pytest.mark.django_db
def test_game_list_view_display(client, sample_game):
    """
    Test sprawdzający, czy widok GameListView poprawnie wyświetla listę gier.
    """
    url = reverse('game_list')
    response = client.get(url)
    content = response.content.decode('utf-8')

    assert response.status_code == 200
    assert sample_game.name in content


@pytest.mark.django_db
def test_game_list_view_filter_form(client):
    """
    Test sprawdzający, czy widok GameListView zawiera formularz filtrowania gier.
    """
    url = reverse('game_list')
    response = client.get(url)
    content = response.content.decode('utf-8')

    assert response.status_code == 200
    assert 'name="number_of_players"' in content
    assert 'name="min_age"' in content
    # Sprawdź obecność pozostałych pól formularza


@pytest.mark.django_db
def test_game_list_filter_functionality(client, sample_game):
    """
    Test sprawdzający funkcjonalność filtrowania w GameListView.
    """
    url = reverse('game_list')
    filter_data = {
        'number_of_players': 4,
        'min_age': 10,
    }
    response = client.get(url, filter_data)
    content = response.content.decode('utf-8')

    assert response.status_code == 200
    assert sample_game.name in content


# **************************************************
# Testy dla widoku MyAccountView
# **************************************************
@pytest.mark.django_db
def test_my_account_view_accessibility(client, user):
    """
    Test sprawdza, czy widok 'Moje konto' jest dostępny tylko dla zalogowanych użytkowników.
    """
    url = reverse('my_account')

    # Test dla niezalogowanego użytkownika
    response = client.get(url)
    assert response.status_code == 302  # Oczekiwane przekierowanie do strony logowania

    # Test dla zalogowanego użytkownika
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200  # Dostęp do strony powinien być możliwy


@pytest.mark.django_db
def test_my_account_view_rentals_display(client, sample_game, user):
    """
    Test dla widoku 'Moje konto' sprawdzający wyświetlanie informacji o wypożyczeniach.

    Test wykonuje następujące kroki:
        1. Dodaje egzemplarz gry do magazynu.
        2. Loguje użytkownika.
        3. Symuluje wypożyczenie gry przez użytkownika poprzez wysłanie żądania POST na widok szczegółów gry.
        4. Przechodzi na stronę 'Moje konto'.
        5. Sprawdza, czy na stronie wyświetlane są informacje o wypożyczonych grach.

    Sprawdza, czy:
        - Nazwa wypożyczonej gry jest widoczna na stronie.
        - Pojawiają się informacje o dacie wypożyczenia i cenie.

    Test ten weryfikuje, czy system poprawnie rejestruje i wyświetla informacje o aktywnych wypożyczeniach użytkownika
    na jego osobistej stronie profilu.
    """
    # Dodanie egzemplarza gry do magazynu i wypożyczenie go
    inventory_item = Inventory.objects.create(game=sample_game, is_rented=False)
    client.login(username=user.username, password='test_password')
    rental_url = reverse('dynamic_game_detail', kwargs={'slug': sample_game.slug})
    client.post(rental_url, {'rent_game': 'true'})

    # Przejście na stronę 'Moje konto'
    my_account_url = reverse('my_account')
    response = client.get(my_account_url)
    content = response.content.decode('utf-8')

    # Sprawdzenie czy na stronie widoczne są informacje o wypożyczonych grach
    assert response.status_code == 200
    assert sample_game.name in content  # Nazwa wypożyczonej gry powinna być widoczna
    assert 'Data wypożyczenia:' in content
    assert 'Cena:' in content


@pytest.mark.django_db
def test_my_account_view_update_user_data(client, user):
    """
    Test sprawdza, czy formularz aktualizacji danych osobowych na stronie 'Moje konto' działa poprawnie.
    """
    client.force_login(user)
    url = reverse('my_account')

    # Przesyłanie danych formularza
    updated_data = {
        'first_name': 'NoweImie',
        'last_name': 'NoweNazwisko',
        'phone_number': '123456789'
        # Dodaj inne pola z formularza, jeśli są wymagane
    }
    response = client.post(url, updated_data)

    # Ponowne pobranie zaktualizowanego użytkownika
    user.refresh_from_db()

    assert response.status_code == 302  # Oczekiwane przekierowanie po aktualizacji
    assert user.first_name == updated_data['first_name']
    assert user.last_name == updated_data['last_name']
    assert user.phone_number == updated_data['phone_number']


@pytest.mark.django_db
def test_my_account_add_address(client, user, sample_address):
    """
    Test sprawdza, czy można poprawnie dodać adres użytkownika na stronie 'Moje konto'.
    """
    client.force_login(user)
    url = reverse('my_account')

    # Dane adresu z fixture sample_address
    address_data = {
        'street': sample_address.street,
        'house_number': sample_address.house_number,
        'postal_code': sample_address.postal_code,
        'city': sample_address.city,
        'country': sample_address.country
    }
    response = client.post(url, address_data)

    # Odświeżenie danych użytkownika
    user.refresh_from_db()

    assert response.status_code == 302  # Oczekiwane przekierowanie po aktualizacji
    assert user.address.street == sample_address.street
    assert user.address.house_number == sample_address.house_number
    assert user.address.postal_code == sample_address.postal_code
    assert user.address.city == sample_address.city
    assert user.address.country == sample_address.country


@pytest.mark.django_db
def test_my_account_update_address(client, user, sample_address):
    """
    Test sprawdza, czy można poprawnie zaktualizować adres użytkownika na stronie 'Moje konto'.
    Najpierw dodaje adres z fixture, a następnie aktualizuje go na nowy.
    """
    client.force_login(user)

    # Dodanie adresu z fixture
    user.address = sample_address
    user.save()

    url = reverse('my_account')

    # Dane nowego adresu
    new_address_data = {
        'street': 'Nowa Ulica',
        'house_number': '2',
        'postal_code': '00-321',
        'city': 'Nowe Miasto',
        'country': 'Nowy Kraj'
    }

    # Wysłanie nowych danych adresowych
    response = client.post(url, new_address_data)

    # Odświeżenie danych użytkownika
    user.refresh_from_db()

    assert response.status_code == 302  # Oczekiwane przekierowanie po aktualizacji
    assert user.address.street == new_address_data['street']
    assert user.address.house_number == new_address_data['house_number']
    assert user.address.postal_code == new_address_data['postal_code']
    assert user.address.city == new_address_data['city']
    assert user.address.country == new_address_data['country']

# **************************************************
# Testy dla widoku RentalListView
# **************************************************
@pytest.mark.django_db
def test_rental_list_view_accessibility_unauthenticated(client):
    """
    Test sprawdza dostępność widoku RentalListView dla niezalogowanego użytkownika.
    """
    url = reverse('rental_list')
    response = client.get(url)
    assert response.status_code == 302  # Oczekiwane przekierowanie lub brak dostępu


@pytest.mark.django_db
def test_rental_list_view_accessibility_regular_user(client):
    """
    Test sprawdza dostępność widoku RentalListView dla zalogowanego użytkownika bez uprawnień pracownika.
    """
    user = CustomUser.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    url = reverse('rental_list')
    response = client.get(url)
    assert response.status_code == 403  # Brak dostępu dla zwykłego użytkownika


@pytest.mark.django_db
def test_rental_list_view_accessibility_staff_user(client, staff_user):
    """
    Test sprawdza dostępność widoku RentalListView dla zalogowanego użytkownika z uprawnieniami pracownika.
    """
    client.login(username=staff_user.username, password='password')

    url = reverse('rental_list')
    response = client.get(url)
    assert response.status_code == 200  # Dostęp powinien być możliwy dla pracownika


@pytest.mark.django_db
def test_rental_list_view_display(client, sample_game, user, staff_user):
    """
    Test sprawdza, czy widok RentalListView poprawnie wyświetla listę wypożyczeń dla pracowników.

    Test wykonuje następujące kroki:
        1. Tworzy egzemplarz gry i dodaje go do magazynu.
        2. Loguje zwykłego użytkownika i symuluje wypożyczenie gry.
        3. Loguje pracownika i przechodzi na stronę listy wypożyczeń.
        4. Sprawdza, czy na liście znajduje się wypożyczona gra.

    Sprawdza, czy:
        - Strona jest dostępna dla pracownika (status HTTP 200).
        - Na stronie znajduje się nazwa wypożyczonej gry, co potwierdza, że lista jest poprawnie wyświetlana.

    Test ten weryfikuje, czy system poprawnie rejestruje wypożyczenia i wyświetla je na liście przeznaczonej
    dla pracowników.
    """
    # Dodanie egzemplarza gry do magazynu
    inventory_item = Inventory.objects.create(game=sample_game, is_rented=False)

    # Wypożyczenie gry przez użytkownika
    client.login(username=user.username, password='test_password')
    rental_url = reverse('dynamic_game_detail', kwargs={'slug': sample_game.slug})
    client.post(rental_url, {'rent_game': 'true'})

    # Logowanie jako pracownik i sprawdzenie listy wypożyczeń
    client.login(username=staff_user.username, password='password')
    rental_list_url = reverse('rental_list')
    response = client.get(rental_list_url)
    content = response.content.decode('utf-8')

    assert response.status_code == 200
    assert sample_game.name in content  # Sprawdzenie, czy nazwa gry jest na liście


@pytest.mark.django_db
def test_rental_list_return_functionality(client, sample_game, user, staff_user):
    """
    Test sprawdza funkcjonalność zwrotu gry na stronie RentalListView dla pracowników.

    Test wykonuje następujące kroki:
        1. Tworzy egzemplarz gry, dodaje go do magazynu, a następnie symuluje wypożyczenie gry przez użytkownika.
        2. Loguje pracownika i przechodzi na stronę listy wypożyczeń.
        3. Wysyła żądanie zwrotu gry poprzez formularz na liście wypożyczeń.
        4. Sprawdza, czy gra została zwrócona i czy została usunięta z listy wypożyczeń.

    Sprawdza, czy:
        - Po zwrocie gry, data zwrotu jest ustawiona w wypożyczeniu.
        - Gra nie jest już widoczna na liście wypożyczeń po zwrocie.

    Test ten weryfikuje, czy system pozwala pracownikom na zarządzanie zwrotami gier i czy lista wypożyczeń
    jest aktualizowana po zwrocie gry.
    """
    # Dodanie egzemplarza gry do magazynu i wypożyczenie go
    inventory_item = Inventory.objects.create(game=sample_game, is_rented=False)
    client.login(username=user.username, password='test_password')
    rental_url = reverse('dynamic_game_detail', kwargs={'slug': sample_game.slug})
    client.post(rental_url, {'rent_game': 'true'})

    # Logowanie jako pracownik
    client.login(username=staff_user.username, password='password')
    rental_list_url = reverse('rental_list')

    # Pobieranie wypożyczenia do zwrotu
    rental = Rental.objects.filter(return_date__isnull=True, user=user).first()

    # Wysłanie żądania zwrotu gry
    return_data = {'return_id': rental.rental_id}
    client.post(rental_list_url, return_data)

    # Sprawdzenie, czy status wypożyczenia został zmieniony na zwrócony
    rental.refresh_from_db()
    assert rental.return_date is not None

    # Ponowne pobranie strony i sprawdzenie, czy gry nie ma już na liście
    response = client.get(rental_list_url)
    content = response.content.decode('utf-8')
    assert sample_game.name not in content  # Gra nie powinna być na liście po zwrocie
