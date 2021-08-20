from typing import List

from pawtrails.core.database import graph
from pawtrails.models.location import Location
from pawtrails.models.pet import Pet
from pawtrails.models.user import User


def prune() -> None:
    print("PRUNNING")
    graph.delete_all()


def seed() -> None:
    prune()
    print("SEEDING USERS")

    users: List[User] = []
    for i in range(0, 5):
        user_in = {
            "email": f"user{i}@example.com",
            "username": f"user{i}",
            "password": "password",
        }
        user = User(**user_in)
        user.save()
        users.append(user)

    print("SEEDING FOLLOWS")  # Make everyone follow everyone
    for i in range(0, 5):
        for j in range(i, 5):
            if i != j:
                users[i].add_following(users[j])
                users[i].save()

    print("SEEDING PETS")
    pets: List[Pet] = []
    for i in range(0, 5):
        pet_in = {
            "name": f"pet{i}",
            "breed": "Dog",
            "energy": 5,
            "size": "Medium",
        }
        pet = Pet(**pet_in)
        pets.append(pet)

    print("SEEDING OWNERS")
    for i in range(0, 5):
        for j in range(i, 5):
            pets[i].add_owner(users[j])
            pets[i].save()

    print("SEEDING LOCATIONS")
    locs: List[Location] = []
    for i in range(0, 5):
        loc_in = {
            "name": f"loc{i}",
            "description": "location",
            "type": "Park",
            "size": "Medium",
            "location": (47.279229, 17.126250),
        }
        loc = Location(**loc_in)
        locs.append(loc)

    for i in range(0, 5):
        locs[i].add_creator(users[i])
        locs[i].save()
