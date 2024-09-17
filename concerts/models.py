import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    ForeignKey,
    create_engine,
    Column,
    Integer,
    String,
    Table,
    Date
)

from sqlalchemy.orm import (
    relationship,
    sessionmaker
)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

connection_str = 'sqlite:///' + os.path.join(BASE_DIR , 'concert.db')

engine = create_engine('sqlite:///concert.db')

Base = declarative_base()

# Sketch of the tables

'''
class Band:
    id : int pk
    name : str
    hometown : str

class venue:
    id : int pk
    title : str
    city : str
'''

# Band Modal

class Band(Base):
    __tablename__ = 'bands'
    id = Column(Integer() , primary_key = True)
    name = Column(String(255) , nullable = False)
    hometown = Column(String(255) , nullable = False)
    # Defining the relationship
    concerts = relationship(
        'Concert', 
        back_populates = 'band'
    )

    def concerts(self):
        return self.concerts

    def venues(self):
        return [concert.venue for concert in self.concerts]
    
    def play_in_venue(self, venue, date):
        concert = Concert(date=date, band=self, venue=venue)
        session.add(concert)
        session.commit()

    def all_introductions(self):
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls):
        return session.query(cls).join(Concert).group_by(cls.id).order_by(func.count().desc()).first()

    def __rep__(self):
        return f"<Band : {self.name}>"
    
    
# Venue Modal

class Venue(Base):
    __tablename__ = 'venues'
    id = Column(Integer() , primary_key = True)
    title = Column(String(255) , nullable = False)
    city = Column(String(255) , nullable = False)
    # Defining the relationship
    concerts = relationship(
        'Concert',
        back_populates = 'venue'
    )

    def concerts(self):
        return self.concerts

    def bands(self):
        return [concert.band for concert in self.concerts]
    
    def concert_on(self, date):
        return session.query(Concert).filter_by(date=date, venue=self).first()

    def most_frequent_band(self):
        band_counts = {}
        for concert in self.concerts:
            band = concert.band
            if band in band_counts:
                band_counts[band] += 1
            else:
                band_counts[band] = 1
        return max(band_counts, key=band_counts.get)
    
    def __repr__(self):
        return f'Venue: {self.title}'
    
# Concert Modal

class Concert(Base):
    __tablename__ = 'concerts'
    id = Column(Integer() , primary_key = True)
    name = Column(String(255) , nullable = False)
    date = Column(String(50) , nullable = False)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue = relationship('Venue', back_populates='concerts')
    band = relationship('Band', back_populates='concerts')

    def band(self):
        return self.band

    def venue(self):
        return self.venue
    
    def hometown_show(self):
        return self.band.hometown == self.venue.city

    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"
    
    def __repr__(self):
        return f'Concert {self.name}'




# Base class
Base.metadata.create_all(engine)