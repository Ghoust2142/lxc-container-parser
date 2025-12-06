from sqlalchemy import Column, integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Container(Base):
    __tablename__ = 'containers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cpu_usager = Column(BigInteger, nullable=False)
    memory_usage = Column(BigInteger, nullable=False)
    created_at_utc = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    ips = relationship(
        "ContainerIP",
        back_populates="container",
        cascade="all, delete-orphan"
    )

class ContainerIP(Base):
    __tablename__ = 'container_ips'

    id = Column(Integer, primary_key=True)
    container_id = Column(Integer, ForeignKey('containers.id'), nullable=False)
    ip_address = Column(String, nullable=False)
    family = Column(String, nullable=True)

    container = relationship("Container", back_populates="ips")
    
      