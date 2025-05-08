from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(30),nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)

    vehicle: Mapped[List["Vehicles"]] = relationship(back_populates="user_vehicles")
    planet: Mapped[List["Planets"]] = relationship(back_populates="user_planets")
    character: Mapped[List["Characters"]] = relationship(back_populates="user_characters")

    favourite: Mapped[List["Favourites"]] = relationship(back_populates="usersFav")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "created_at": self.created_at.isoformat(),
            "vehicle": [vehic.serialize() for vehic in self.vehicle],
            "planet": [pla.serialize() for pla in self.planet],
            "character": [charact.serialize() for charact in self.character],
            "favourite": [fav.serialize() for fav in self.favourite]
        }

class Vehicles(db.Model):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    model: Mapped[str] = mapped_column(String(80), nullable=False)
    cost_credits: Mapped[str] = mapped_column(String(30), nullable=False)
    max_speed: Mapped[str] = mapped_column(String(30), nullable=False)
    crew: Mapped[str] = mapped_column(String(30), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_vehicles: Mapped["Users"] = relationship(back_populates="vehicle")

    favourite: Mapped[List["Favourites"]] = relationship(back_populates="vehiclesFav")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "cost_credits": self.cost_credits,
            "max_speed": self.max_speed,
            "crew": self.crew,
            "user_vehicles": self.user_vehicles.username,
            "favourite": [fav.serialize() for fav in self.favourite]
        }

class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    climate: Mapped[str] = mapped_column(String(80), nullable=False)
    population: Mapped[str] = mapped_column(String(30), nullable=False)
    terrain: Mapped[str] = mapped_column(String(30), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_planets: Mapped["Users"] = relationship(back_populates="planet")

    favourite: Mapped[List["Favourites"]] = relationship(back_populates="planetsFav")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain,
            "user_planets": self.user_planets.username,
            "favourite": [fav.serialize() for fav in self.favourite]
        }

class Characters(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    gender: Mapped[str] = mapped_column(String(80), nullable=False)
    height: Mapped[str] = mapped_column(String(30), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(30), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=False)
    eyes_color: Mapped[str] = mapped_column(String(50), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_characters: Mapped["Users"] = relationship(back_populates="character")

    favourite: Mapped[List["Favourites"]] = relationship(back_populates="charactersFav")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "birth_year": self.birth_year,
            "skin_color": self.skin_color,
            "eyes_color": self.eyes_color,
            "user_characters": self.user_characters.username,
            "favourite": [fav.serialize() for fav in self.favourite]
        }
    
class Favourites(db.Model):
    __tablename__ = "favourites"
    usersFav_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    vehiclesFav_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), primary_key=True)
    planetsFav_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), primary_key=True)
    charactersFav_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), primary_key=True)
    
    date: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)

    usersFav: Mapped["Users"] = relationship(back_populates="favourite")
    vehiclesFav: Mapped["Vehicles"] = relationship(back_populates="favourite")
    planetsFav: Mapped["Planets"] = relationship(back_populates="favourite")
    charactersFav: Mapped["Characters"] = relationship(back_populates="favourite")

    def serialize(self):
        return {
            "usersFav_id": self.usersFav_id,
            "vahiclesFav_id": self.vahiclesFav_id,
            "planetsFav_id": self.planetsFav_id,
            "charactersFav_id": self.usersFav_id,
            "date": self.date.isoformat(),
        }
