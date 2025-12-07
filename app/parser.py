import json
from datetime import datetime, timezone
from typing import List

# Importujeme naše Pydantic datové třídy,
# do kterých budeme ukládat parsovaná data.
from .schemas import ContainerDTO, ContainerIPDTO


def to_utc_timestamp(dt_str: str) -> int:
    """
    Funkce vezme datum jako text (string),
    které je v ISO formátu včetně časové zóny,
    převede ho na Python datetime
    a následně ho převádí do UTC timezone.
    Nakonec vrací timestamp jako celé číslo.
    """
    # převedu textové datum na datetime objekt
    dt = datetime.fromisoformat(dt_str)

    # převedu čas do UTC, aby byl všude stejný
    dt_utc = dt.astimezone(timezone.utc)

    # vrátím jako integer timestamp
    return int(dt_utc.timestamp())


def parse_containers(json_path: str) -> List[ContainerDTO]:
    """
    Funkce otevře JSON soubor, ve kterém je seznam kontejnerů.
    Každý kontejner rozparsujeme a vrátíme jako ContainerDTO.
    Výsledkem je seznam všech DTO objektů.
    """

    # otevřu JSON soubor a načtu data jako Python list/dict strukturu
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # tady budeme postupně přidávat objekty ContainerDTO
    containers: List[ContainerDTO] = []

    # projdeme si každý kontejner v JSONu
    for item in data:

        # název kontejneru – mělo by být vždy v JSONu, proto item["name"]
        name = item["name"]

        # původní datum vytvoření (je to string)
        created_at_raw = item["created_at"]

        # status kontejneru, pokud tam není, dáme "unknown"
        status = item.get("status", "unknown")

        # state může být None (např. kontejner není spuštěný),
        # proto pokud je None, nastavíme na prázdný slovník {}
        state = item.get("state") or {}

        # načteme CPU usage, pokud tam není, nastavíme na 0
        cpu_usage = state.get("cpu", {}).get("usage", 0)

        # načteme RAM usage, pokud není, také dáme 0
        memory_usage = state.get("memory", {}).get("usage", 0)

        # tady budeme ukládat všechny IP adresy kontejneru
        ips: List[ContainerIPDTO] = []

        # získáme "network" část z JSONu; když chybí, nastavíme prázdný dict
        network = state.get("network") or {}

        # projdeme všechny síťové rozhraní (např. eth0, eth1)
        for iface in network.values():

            # každé rozhraní má seznam adres (IPv4 i IPv6)
            for addr in iface.get("addresses", []):

                # samotná IP adresa
                ip_address = addr.get("address")
                # rodina adresy (inet = IPv4, inet6 = IPv6)
                family = addr.get("family")

                # pokud existuje adresa, uložíme ji
                if ip_address:
                    ips.append(
                        ContainerIPDTO(
                            ip_address=ip_address,
                            family=family,
                        )
                    )

        # vytvoříme ContainerDTO objekt se všemi daty, které jsme nasbírali
        container_dto = ContainerDTO(
            name=name,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            created_at_utc=to_utc_timestamp(created_at_raw),
            status=status,
            ips=ips,
        )

        # přidáme do seznamu výsledků
        containers.append(container_dto)

    # vrátíme list všech parsovaných kontejnerů
    return containers


# Tady je jednoduchý test, aby se dalo script spustit samostatně
if __name__ == "__main__":
    parsed = parse_containers("sample-data.json")
    print(f"Načteno kontejnerů: {len(parsed)}")

    # vytiskneme první položku, abychom viděli, jak to vypadá
    if parsed:
        print(parsed[0].model_dump())

