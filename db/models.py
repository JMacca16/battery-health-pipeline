import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PackReading(Base):
    __tablename__ = "pack_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    pack_id = Column(String, nullable=False)
    cycle_count = Column(Integer, nullable=False)
    state = Column(String, nullable=False)
    pack_voltage = Column(Float, nullable=False)
    pack_current = Column(Float, nullable=False)


class CellReading(Base):
    __tablename__ = "cell_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    pack_id = Column(String, nullable=False)
    battery_id = Column(String, nullable=False)
    voltage = Column(Float, nullable=False)
    current = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    soc = Column(Float, nullable=False)
    soh = Column(Float, nullable=False)
    nominal_capacity = Column(Float, nullable=False)
    available_capacity = Column(Float, nullable=False)
    internal_resistance = Column(Float, nullable=False)
    cycle_count = Column(Integer, nullable=False)
    state = Column(String, nullable=False)
    is_anomaly = Column(Boolean, nullable=False)
