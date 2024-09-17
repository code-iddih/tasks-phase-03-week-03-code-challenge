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

# The association table
concerts_table = Table(
    'concerts',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('band_id', Integer, ForeignKey('bands.id')),
    Column('venue_id', Integer, ForeignKey('venues.id')),
    Column('concert_date', Date)
)

# Band Modal

class Band(Base):
    __tablename__ = 'bands'
    id = Column(Integer() , primary_key = True)
    name = Column(String(255) , nullable = False)
    hometown = Column(String(255) , nullable = False)
    # Defining the relationship
    venues = relationship(
        'Venue', 
        secondary = concerts_table,
        back_populates = 'bands'
    )

    def __rep__(self):
        return f"<Band : {self.name}>"
    
# Venue Modal

class Venue(Base):
    __tablename__ = 'venues'
    id = Column(Integer() , primary_key = True)
    title = Column(String(255) , nullable = False)
    city = Column(String(255) , nullable = False)
    # Defining the relationship
    bands = relationship(
        'Band',
        secondary = concerts_table,
        back_populates = 'venues'
    )

    def __rep__(self):
        return f"<Venue : {self.title}>"


# Base class
Base.metadata.create_all(engine)