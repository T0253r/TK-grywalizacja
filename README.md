# nazwa robocz: projekt grywalizacja

Ten projekt został stworzony na potrzeby koła naukowego TK Games //dodać jakiś link//  
przez:
- @zeolsem
- @T0253r
- @my-december
- @p0mpon

### Jak uruchomić projekt
1. `git clone <link_który_macie_jak_klikniecie_na_zielony_przycisk_code>` - klonuje repozytorium na wasz komputer
2. `cd <nazwa_repozytorium>` - wchodzi do folderu z repozytorium
3. Stwórzcie środowisko wirtualne
   - `python3 -m venv venv` - tworzy venv w folderze z repozytorium
   - `source venv/bin/activate` - aktywuje venv (na windowsie `venv\Scripts\activate`, i pewnie nie source)
4. `pip install -r requirements.txt` - instaluje wszystkie zależności
5. `flask --app app run --debug` - uruchamia aplikację

### Jak pracować w projekcie

yap yap yap
Narazie tylko dla was to jest więc powiem jak pracować  

Wersja alternatywna: https://docs.solvro.pl/solvro/git-basics/intro/  

Workflow:
1. `git switch main` - (jakbyście nie byli na main)
2. `git pull main` - pobiera najnowsze zmiany
3. `git checkout -b <nazwa_gałęzi>` - tworzy nową gałąź
4. Tam sobie piszecie jakiś kodzik
5. `git add .` - dodaje wszystkie zmiany do commita
6. `git commit -m "<nazwa>"` - tworzy commit z dodanymi zmianami, przykładowe nazwy to:
"feat: dodanie importu plików json", "fix: naprawa layoutu drzewek", "refactor: zmiana koloru tła",
lepiej chyba po angielsku tho, ale jak wolicie
7. `git push --set-upstream origin <nazwa_gałęzi>` - wysyła zmiany na zdalne repozytorium,  
przy czym **flagę --set-upstream** dodajemy tylko przy pierwszym pushu na nową gałąź, aby ją utworzyć
w zdalnym repozytorium**
8. Na GitHubie powinno się wyświetlić że gałąź miała niedawno pushe i klikamy przycisk `Compare & pull request`
9. Można tam dodać komentarz, można zmergować od razu (**najlepiej tylko squash & merge albo rebase & merge**)  
Możecie też oznaczyć kogoś do code review, aby przejrzał zmiany i zaakceptował (taką default osobą mogę być ja)
**Uwaga**: gdybyście chcieli pushować po dłuższym czasie, to po commicie wróćcie najpierw na main, zróbcie na mainie
`git pull`, przejdźcie z powrotem na swoją gałąź i użyjcie `git rebase main`, aby zaktualizować swoją gałąź do
najnowszych zmian. Gdyby pojawiły się konflikty to możecie się odwołać do ostatniej części tego tutoriala:
https://docs.solvro.pl/solvro/git-basics/intro/  
10. Jak już zmergujecie to możecie usunąć swoją gałąź

Gdyby to było nieskładne (a pewnie jest bo robię speedrun), to myślę, że ten poradnik, który podlinkowałem
napisałem dosyć zrozumiale.