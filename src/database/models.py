from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()

class Artist(Base): 
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    first = Column(String(50))
    last = Column(String(50))
    birth = Column(Integer)
    death = Column(Integer)
    nickname = Column(String(50))
    artworks = relationship("Artwork", back_populates="artists")
    nation = Column(String(50))

    def __repr__(self):
        return "<User(fullname='%s', nation='%s')>" % (self.first + " " +  self.last, self.nation)  

class Artwork(Base):
    __tablename__ = 'artworks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    location = Column(String)
    medium = Column(String)
    artist_id = Column(Integer, ForeignKey('artist.id'), nullable=False)
    artist = relationship("Artist", back_populates="artworks")

    def __repr__(self):
        return "<Artwork(name='%s', year='%s', artist='%s')>" % (self.name, self.year, self.artist.last)



