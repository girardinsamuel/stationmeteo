from datetime import datetime
from app import db, Sensor, Log, app

with app.app_context():
    db.drop_all()
    db.create_all()

    sensor1 = Sensor(name="Maison", id=1, simple=True)
    sensor2 = Sensor(name="Jardin", id=2, simple=False)
    sensor3 = Sensor(name="Gîte", id=3, simple=True)

    db.session.add_all([sensor1, sensor2, sensor3])
    db.session.commit()
