from sqlalchemy.ext.declaritive import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()


# Artist - describes the individual behind one or more works of art
#
# id: unique id of artist
# first: first name of artist
# last: last name of artist
# nickname: public name of artist
# gender: gender of artist
# artworks: associated artwork objects
# nation_id: unique id of nation associated with the artist
# nation: associated nation object
# movement_id: unique id of movement associated with artist
# movement: movement object associated with the artist
class Artist(Base): 
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    first = Column(String)
    last = Column(String)
    birth = Column(Integer)
    death = Column(Integer)
    nickname = Column(String)
    artworks = relationship("Artwork", back_populates="artists")
    nation_id = Column(Integer, ForeignKey('nation.id'))
    nation = relationship("Nation", back_populates="artists")


# Artwork - describes an artwork produced by an individual artist
# 
# id: unique id of artwork
# name: the name of the artwork
# year: the year the artwork was created
# artist_id: unique id of artist responsible for artwork
# artist: association with artist responsible for artwork
# medium_id: unique id of medium used to create the artwork
# medium: associated medium of artwork
# subject_category: associated subject category of artwork (see Category)
# subject_category_id: unique id of subject associated with artwork
# location_id: id of location associated with artwork
# location: location object associated with the artwork
class Artwork(Base):
    __tablename__ = 'artworks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship("Artist", back_populates="artworks")
    medium_id = Column(Intger, ForeignKey('medium.id'))
    medium = relationship("Medium", back_populates="artworks")
    subject_category_id = Column(Integer, ForeignKey('subject_category.id'))
    subject_category = relationship("Subject_Category", back_populates="artworks")
    location_id = Column(Integer, ForeignKey('subject_category.id'))
    location = relationship("Location", back_populates="artworks")



# Subject_Category - describes the subject_category of a given artwork (portrait/religious/historic/still-life/etc...)
#
# id: unique id of the subject category
# name: name of subject category
# artworks: all artworks associated with category
class Subject_Category(Base):
    __tablename__ = 'subject_categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    artworks = relationship("Artwork", back_populates="subject_categories")
    
# Medium - describes the material used to produce an artwork
# 
# id: unique id of medium
# name: name of medium (oil on canvas/pastel/pen/pencil/etc...)
# artworks: artworks associated with the medium
class Medium(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    artworks = relationship("Artwork", back_populates="media")
   
# Country - describes a nation which artists or users belong to
# 
# id: unique id of medium
# name: name of country
# nationality: label used to describe people or items from nation
# continent_id: the id of the continent the nation belongs to
# continent: the associated continent of the country
# artists: the artists associated with the country
class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nationality = Column(String)
    continent_id = (Integer, ForeignKey('continent.id'))
    continent = relationship("Continent", back_populates="countries")
    artists = relationship("Artist", back_populates="countries")

# Continent - describes a continent which nations belong to
#
# id: unique id of continent
# name: name of continent
# countries: countries belonging to continent
class Continent(Base):
    __tablename__ = 'continents'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    countries = relationship("Country", back_populates="continents")

# Movements - describes an artistic movement that art or artists are associated with
# 
# id: unique id of movement
# name: name or movement
# description: description of artistic movement
# artists: artists associated with artistic movement
class Movement(Base):
    __tablename__ = 'movements'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    artists = relationship("Artist", back_populates="movements")

# Display_Location - the museum or gallery that the art is currently located in
#
# id: unique id of location
# name: the name of the location
# description: 
# artworks: the artworks found at the location
# nation_id: id of the nation the location is located in
# nation: the nation the location is located in 
class Display_Location(Base):
    __tablename__ = 'display_locations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    artworks = relationship("Artwork", back_populates="display_locations")
    nation_id = Column(Integer, ForeignKey('nation.id'))
    nation = relationship("Nation", back_populates="nations")
