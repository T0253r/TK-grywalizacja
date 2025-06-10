# Projekt Grywalizacja

Ten projekt został stworzony na potrzeby koła naukowego TK Games
przez:
- @zeolsem
- @T0253r
- @my-december
- @p0mpon

Celem projektu jest utworzenie webaapki, w której członkowie koła nukowego będą mogli przeglądać i wykonywac zadania przezentowane w formie drzewek umiejętności. Wykonanie zadania może weryfikować admin. Za zweryfikowane zadania użytkownicy otrzymują punkty zliczane w rankingu. Webappka wpiera logowanie poprzez platformę discord.

### Jak uruchomić projekt
(Wymaga kluczy w pliku .env oraz podłączonej aplikacji Discord w Developer Portal)
1. `pip install -r requirements.txt` - instaluje wszystkie zależności
2. `python showcase_init.py` - inicjuje przykładową bazę danych
3. `flask --app grywalizacja_app run --debug` OR `python run.py` - uruchamia aplikację
