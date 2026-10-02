## Automatisk insamling av väderprognoser

Ett GitHub Actions-flöde (`.github/workflows/samla_prognos.yml`) hämtar SMHI:s väderprognos för Malmö A varje timme, kvart över, och sparar de närmaste 24 timmarna i `prognosinsamling/prognoser/`, en fil per dygn.

Varje rad innehåller:
- `referenceTime`: vilken prognoskörning raden kommer från
- `hamtad_utc`: när prognosen hämtades
- `timmar_fram`: hur många timmar efter referenceTime prognosen gäller

**Viktigt:** Flödet committar ny data till repot varje timme. Kör alltid `git pull` innan du börjar arbeta, annars uppstår konflikter när du pushar.

Flödet kan också startas manuellt under fliken **Actions** på GitHub.