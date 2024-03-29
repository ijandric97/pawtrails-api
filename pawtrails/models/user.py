from __future__ import annotations

import operator
import textwrap
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from neotime import DateTime
from py2neo.data.spatial import WGS84Point
from py2neo.ogm import Property, RelatedFrom, RelatedTo
from pydantic import BaseModel as Schema
from pydantic import EmailStr
from pydantic.fields import Field
from typing_extensions import Annotated

from pawtrails.core.database import BaseModel, BaseSchema, graph, repository
from pawtrails.core.security import get_password_hash, verify_password

if TYPE_CHECKING:
    from pawtrails.models.location import Location
    from pawtrails.models.pet import Pet
    from pawtrails.models.review import Review


class User(BaseModel):
    # TODO: Actually set this to false until user activates with mail
    # TODO: email on registering, use AWS for that
    full_name = Property(key="full_name", default="")
    is_active = Property(key="is_active", default=True)
    _email = Property(key="email")
    _username = Property(key="username")
    _password = Property(key="password")
    _home = Property(key="home")

    # NOTE: Import this whole things so there is not CIRCULAR IMPORTS
    _following = RelatedTo("pawtrails.models.user.User", "FOLLOWS")
    _followers = RelatedFrom("pawtrails.models.user.User", "FOLLOWS")
    _pets = RelatedTo("pawtrails.models.pet.Pet", "OWNS")
    _locations = RelatedTo("pawtrails.models.location.Location", "CREATED")
    _favorites = RelatedTo("pawtrails.models.location.Location", "FAVORITED")
    _reviews = RelatedTo("pawtrails.models.review.Review", "WROTE")

    @classmethod
    def get_by_is_active(
        cls, is_active: bool, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return [
            user
            for user in cls.match(repository)
            .where(is_active=is_active)
            .skip(skip)
            .limit(limit)
            .all()
        ]

    @classmethod
    def get_by_email(cls, email: str) -> Optional[User]:
        return cls.match(repository).where(email=email).first()

    @classmethod
    def get_by_username(cls, username: str) -> Optional[User]:
        return cls.match(repository).where(username=username).first()

    @classmethod
    def authenticate(cls, email: str, password: str) -> Optional[User]:
        user = cls.get_by_email(email=email)
        if not user or not verify_password(password, user.password):
            return None
        return user

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        if not isinstance(email, str):
            raise TypeError(f"Email {email} is not an email.")
        if User.get_by_email(email):
            raise ValueError(f"Email {email} already exists.")
        self._email = email

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        if not isinstance(username, str):
            raise TypeError(f"Username {username} is not a string.")
        if User.get_by_username(username):
            raise ValueError(f"Username {username} already exists.")
        self._username = username

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        if not isinstance(password, str):
            raise TypeError(f"Password {password} is not a string.")
        self._password = get_password_hash(password)

    @property
    def following(self) -> List[User]:
        return [follow for follow in self._following]

    @property
    def following_count(self) -> int:
        return len(self._following)

    def add_following(self, user: User) -> bool:
        if self == user or user in self._following:
            return False
        self._following.add(user, created_at=DateTime.utc_now())
        return True

    def remove_following(self, user: User) -> bool:
        if self == user or user not in self._following:
            return False
        self._following.remove(user)
        return True

    @property
    def followers(self) -> List[User]:
        return [follow for follow in self._followers]

    @property
    def followers_count(self) -> int:
        return len(self._followers)

    @property
    def pets(self) -> List[Pet]:
        return [pet for pet in self._pets]

    def add_pet(self, pet: Pet) -> bool:
        if pet in self._pets:
            return False
        self._pets.add(pet, created_at=DateTime.utc_now())
        return True

    def remove_pet(self, pet: Pet) -> bool:
        if pet not in self._pets:
            return False
        self._pets.remove(pet)
        return True

    @property
    def locations(self) -> List[Location]:
        # TODO: Think about how to approach add, remove functions??
        return [location for location in self._locations]

    @property
    def favorites(self) -> List[Location]:
        return [location for location in self._favorites]

    def add_favorite(self, location: Location) -> bool:
        if location in self._favorites:
            return False
        self._favorites.add(location, created_at=DateTime.utc_now())
        return True

    def remove_favorite(self, location: Location) -> bool:
        if location not in self._favorites:
            return False
        self._favorites.remove(location)
        return True

    @property
    def home(self) -> Optional[WGS84Point]:
        if self._home:
            return WGS84Point((self._home[0], self._home[1]))
        return None

    def set_home(self, longitude: float, latitude: float) -> None:
        if not isinstance(longitude, float):
            raise TypeError(f"Longitude {longitude} is not a float.")
        if not isinstance(latitude, float):
            raise TypeError(f"Latitude {latitude} is not a float.")
        self._home = WGS84Point((longitude, latitude))

    def remove_home(self) -> None:
        self._home = None

    # TODO: Add endpoints for this

    @property
    def reviews(self) -> List[Review]:
        return [review for review in self._reviews]

    # TODO: Add a save checking function
    def get_dashboard(self) -> List[DashboardSchema]:
        my_query: str = f'MATCH (me:User {{ uuid: "{self._uuid}" }})\n'
        my_query += textwrap.dedent(
            """
            MATCH (me)-[owns:OWNS]-(pet:Pet)
            WITH me, pet.name as mpn,
            owns.created_at as mpt, pet.uuid as mpu

            MATCH (me)-[created:CREATED]->(loc:Location)
            WITH me, mpn, mpt, mpu, loc.name as mln,
            created.created_at as mlt, loc.uuid as mlu

            MATCH (me)-[favorited:FAVORITED]->(fav_loc:Location)
            WITH me, mpn, mpt, mpu, mln, mlt, mlu,
            fav_loc.name as mfn, favorited.created_at as mft, fav_loc.uuid as mfu

            MATCH (me)-[wrote:WROTE]-(review:Review)-[:FOR]->(rew_loc:Location)
            WITH me, mpn, mpt, mpu, mln, mlt, mlu, mfn, mft, mfu,
            rew_loc.name as mrn, wrote.created_at as mrt, rew_loc.uuid as mru

            RETURN
            collect(DISTINCT {
                user: "You",
                user_uuid: me.uuid,
                action: "created",
                label: "pet",
                name: mpn,
                time: mpt,
                uuid: mpu
            }) as my_pets,
            collect(DISTINCT {
                user: "You",
                user_uuid: me.uuid,
                action: "reviewed",
                label: "location",
                name: mrn,
                time: mrt,
                uuid: mru
            }) as my_reviews,
            collect(DISTINCT {
                user: "You",
                user_uuid: me.uuid,
                action: "created",
                label: "location",
                name: mln,
                time: mlt,
                uuid: mlu
            }) as my_locations,
            collect(DISTINCT {
                user: "You",
                user_uuid: me.uuid,
                action: "favorited",
                label: "location",
                name: mfn,
                time: mft,
                uuid: mfu
            }) as my_fav_locations"""
        )
        user_query: str = (
            f'\nMATCH (:User {{ uuid: "{self._uuid}" }})-[:FOLLOWS]->(user:User)\n'
        )
        user_query += textwrap.dedent(
            """
            MATCH (user)-[owns:OWNS]-(pet:Pet)
            WITH user, pet.name as mpn,
            owns.created_at as mpt, pet.uuid as mpu

            MATCH (user)-[created:CREATED]->(loc:Location)
            WITH user, mpn, mpt, mpu, loc.name as mln,
            created.created_at as mlt, loc.uuid as mlu

            MATCH (user)-[favorited:FAVORITED]->(fav_loc:Location)
            WITH user, mpn, mpt, mpu, mln, mlt, mlu,
            fav_loc.name as mfn, favorited.created_at as mft, fav_loc.uuid as mfu

            MATCH (user)-[wrote:WROTE]-(review:Review)-[:FOR]->(rew_loc:Location)
            WITH user, mpn, mpt, mpu, mln, mlt, mlu, mfn, mft, mfu,
            rew_loc.name as mrn, wrote.created_at as mrt, rew_loc.uuid as mru

            RETURN
            collect(DISTINCT {
                user: user.username,
                user_uuid: user.uuid,
                action: "created",
                label: "pet",
                name: mpn,
                time: mpt,
                uuid: mpu
            }) as pets,
            collect(DISTINCT {
                user: user.username,
                user_uuid: user.uuid,
                action: "reviewed",
                label: "location",
                name: mrn,
                time: mrt,
                uuid: mru
            }) as reviews,
            collect(DISTINCT {
                user: user.username,
                user_uuid: user.uuid,
                action: "created",
                label: "location",
                name: mln,
                time: mlt,
                uuid: mlu
            }) as locations,
            collect(DISTINCT {
                user: user.username,
                user_uuid: user.uuid,
                action: "favorited",
                label: "location",
                name: mfn,
                time: mft,
                uuid: mfu
            }) as fav_locations
            """
        )

        updates: List[DashboardSchema] = []

        def iterate_records(query: str, updates: list) -> None:
            for records in graph.run(query):
                for subrecords in records:
                    for update in subrecords:
                        updates.append(
                            DashboardSchema(
                                user=update["user"],
                                user_uuid=update["user_uuid"],
                                action=update["action"],
                                label=update["label"],
                                name=update["name"],
                                time=str(update["time"]),
                                uuid=update["uuid"],
                            )
                        )

        iterate_records(my_query, updates)
        iterate_records(user_query, updates)

        updates.sort(key=operator.attrgetter("time"), reverse=True)

        return updates


class UserSchema(BaseSchema):
    full_name: Optional[str]
    username: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_active: Optional[bool] = True
    following_count: Optional[int]
    followers_count: Optional[int]


class UserFullSchema(UserSchema):
    email: Optional[EmailStr]
    home: Optional[WGS84Point]
    # following: Optional[List[UserSchema]]
    # pets: Optional[List[PetSchema]]


class AddUserSchema(Schema):
    email: EmailStr = Field(example="user@example.com")
    username: Annotated[str, Field(example="user", min_length=3)]
    password: Annotated[str, Field(example="password", min_length=8)]


class UpdateUserSchema(Schema):
    email: Optional[EmailStr] = Field(example="user@example.com")
    username: Annotated[Optional[str], Field(example="user", min_length=3)]
    password: Annotated[Optional[str], Field(example="password", min_length=8)]
    old_password: Annotated[Optional[str], Field(example="password", min_length=8)]
    full_name: Optional[str]
    home_longitude: Optional[float]
    home_latitude: Optional[float]


class DashboardSchema(Schema):
    user: str = ""
    user_uuid: str = ""
    action: str = ""
    label: str = ""
    name: str = ""
    time: str = ""
    uuid: str = ""
