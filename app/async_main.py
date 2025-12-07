import asyncio
from typing import List

from .parser import parse_containers
from .schemas import ContainerDTO
from .models import Container, ContainerIP
from .db_async import AsyncSessionLocal, init_db_async


async def save_containers_to_db_async(containers: List[ContainerDTO]) -> None:
    """
    Async varianta uložení ContainerDTO do databáze.
    Používá AsyncSession z SQLAlchemy.
    """
    async with AsyncSessionLocal() as session:
        try:
            for dto in containers:
                container_obj = Container(
                    name=dto.name,
                    cpu_usage=dto.cpu_usage,
                    memory_usage=dto.memory_usage,
                    created_at_utc=dto.created_at_utc,
                    status=dto.status,
                )
                session.add(container_obj)

                # flush pro získání ID (async varianta)
                await session.flush()

                for ip_dto in dto.ips:
                    ip_obj = ContainerIP(
                        container_id=container_obj.id,
                        ip_address=ip_dto.ip_address,
                        family=ip_dto.family,
                    )
                    session.add(ip_obj)

            await session.commit()
            print("Ukládání do databáze (async) dokončeno.")
        except Exception as e:
            await session.rollback()
            print("Chyba při ukládání do databáze (async):", e)


async def async_main() -> None:
    """
    Async vstupní bod:
    - inicializuje DB
    - naparsuje JSON
    - uloží data do DB pomocí async session
    """
    await init_db_async()

    json_path = "sample-data.json"
    containers: List[ContainerDTO] = parse_containers(json_path)
    print(f"Naparsováno kontejnerů: {len(containers)}")

    await save_containers_to_db_async(containers)


if __name__ == "__main__":
    asyncio.run(async_main())
