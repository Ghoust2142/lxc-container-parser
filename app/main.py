from typing import List

# Naimportujeme si věci z našeho projektu:
# - init_db a SessionLocal pro práci s databází
# - SQLAlchemy modely Container a ContainerIP
# - funkci parse_containers, která načte JSON a vrátí DTO objekty
from .db import init_db, SessionLocal
from .models import Container, ContainerIP
from .parser import parse_containers
from .schemas import ContainerDTO


def save_containers_to_db(containers: List[ContainerDTO]) -> None:
    """
    Funkce vezme list ContainerDTO (tedy výsledek z parseru)
    a uloží je do databáze pomocí SQLAlchemy modelů.
    """

    # Vytvoříme novou databázovou session.
    # Přes session pak budeme dělat INSERT do tabulek.
    session = SessionLocal()

    try:
        # projdeme všechny kontejnery, které jsme naparsovali z JSONu
        for dto in containers:
            # vytvoříme SQLAlchemy objekt pro tabulku 'containers'
            container_obj = Container(
                name=dto.name,
                cpu_usage=dto.cpu_usage,
                memory_usage=dto.memory_usage,
                created_at_utc=dto.created_at_utc,
                status=dto.status,
            )

            # přidáme ho do session (zatím ještě neuložený do DB)
            session.add(container_obj)

            # flush pošle INSERT do DB, ale necommitne transakci.
            # díky tomu získáme vyplněné id (primární klíč).
            session.flush()

            # teď můžeme uložit IP adresy navázané na tento kontejner
            for ip_dto in dto.ips:
                ip_obj = ContainerIP(
                    container_id=container_obj.id,
                    ip_address=ip_dto.ip_address,
                    family=ip_dto.family,
                )
                session.add(ip_obj)

        # pokud bylo všechno v pořádku, tak změny commitneme
        session.commit()

    except Exception as e:
        # pokud se něco pokazí, vrátíme změny zpět (rollback)
        session.rollback()
        # vypíšeme chybu do konzole, aby bylo vidět, co se děje
        print("Chyba při ukládání do databáze:", e)
        # v reálné aplikaci bychom možná chybu logovali a zvedli výjimku dál

    finally:
        # ať už to dopadlo jakkoliv, session zavřeme
        session.close()


def main() -> None:
    """
    Hlavní vstupní bod skriptu.
    1) Inicializuje databázi (vytvoří tabulky).
    2) Naparsuje JSON soubor.
    3) Uloží data do databáze.
    """

    # Inicializace databáze – vytvoří tabulky podle modelů.
    # Pokud už existují, nic se nestane.
    init_db()

    # Naparsujeme JSON soubor se seznamem kontejnerů.
    # Předpokládáme, že sample-data.json leží v rootu projektu.
    json_path = "sample-data.json"
    containers = parse_containers(json_path)

    print(f"Naparsováno kontejnerů: {len(containers)}")

    # Uložíme DTO objekty do databáze.
    save_containers_to_db(containers)

    print("Ukládání do databáze dokončeno.")


# Díky tomuhle bloku můžeme skript spustit příkazem:
# py -m app.main
if __name__ == "__main__":
    main()


