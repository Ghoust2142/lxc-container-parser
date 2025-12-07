import os
from dotenv import load_dotenv 

# Načtme proměnné z .env souboru (v rootu projektu)
load_dotenv()

# DATABASE_URL budeme mít v .env souboru
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://lxc_user:lxc_pass@localhost:5432/lxc_db"
)

