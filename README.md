# LXC Container Parser (TeskaLabs)

Jednoduchá Python aplikace pro parsování seznamu LXC kontejnerů (JSON) a ukládání dat do PostgreSQL databáze.

Součástí projektu je i základní dockerizace – PostgreSQL běží v Docker kontejenru.

Použité technologie:

Python 3.13
Pydantic – validace dat a DTO modely
SQLAlchemy 2.0 – ORM vrstva pro práci s databází
PostgreSQL 16 – relační databáze
Docker / Docker Compose – spuštění databáze
psycopg2-binary – PostgreSQL driver

Struktura projektu: 

app/
  ├── parser.py        # Parsování JSON → ContainerDTO
  ├── schemas.py       # Pydantic DTO modely
  ├── models.py        # SQLAlchemy tabulky (containers + container_ips)
  ├── db.py            # DB engine + session
  └── main.py          # Uložení naparsovaných dat do PostgreSQL
docker-compose.yml      # Postgres databáze
requirements.txt        # Python závislosti
sample-data.json        # Vstupní data (LXC kontejnery)

Spuštění databáze v Dockeru

V kořenové složce projektu:
bash přikaz: docker compose up -d db


Kontrola běžícího kontejneru:
bash přikaz: docker ps

Spuštění parseru (bez databáze):
bash přikaz: py -m app.parser


Parser vypíše počet naparsovaných kontejnerů a ukázková data.
Uložení kontejnerů do PostgreSQL

S databází běžící v Dockeru:
bash přikaz: py -m app.main