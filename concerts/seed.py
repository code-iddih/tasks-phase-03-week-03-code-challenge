import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Band, Venue
from datetime import date

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

connection_str = 'sqlite:///' + os.path.join(BASE_DIR, 'concert.db')

engine = create_engine(connection_str)

Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()

# creating instances of classes to test code

band1 = Band(name="Acapella", hometown="Nairobi")
band2 = Band(name="Sauti Sol", hometown="Nakuru")
band3 = Band(name="Mbogi Genje", hometown="Eldoret")

venue1 = Venue(title="Kasarani Square", city="Nairobi")
venue2 = Venue(title="Nyayo Stadium", city="Nakuru")
venue3 = Venue(title="Jacaranda Stadium", city="Los Angeles")

band1.venues.append(venue1)
band2.venues.append(venue2)
band3.venues.append(venue3)


session.add_all([band1, band2, band3])

session.commit()

session.close()

print("Seeding Successfull...")
