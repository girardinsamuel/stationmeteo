from sqlalchemy.orm import Mapped, mapped_column
from app import db


class Sensor(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    simple: Mapped[bool] = mapped_column()


class DataLog(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column()
    temperature: Mapped[float] = mapped_column()
    pressure: Mapped[float] = mapped_column()
    humidity: Mapped[float] = mapped_column()
    rain: Mapped[float] = mapped_column()
    light: Mapped[float] = mapped_column()
    battery: Mapped[int] = mapped_column()
    sensor = db.relationship("Sensor", backref="data_logs")
