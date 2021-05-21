from typing import List

from pawtrails.core.database import graph  # noqa
from pawtrails.models.pet import Pet
from pawtrails.models.user import User


def prune() -> None:
    print("PRUNNING")
    graph.delete_all()


def seed() -> None:
    print("SEEDING USERS")

    users: List[User] = []
    for i in range(0, 5):
        user_in = {
            "email": f"user{i}@example.com",
            "username": f"user{i}",
            "password": "password",
        }
        users.append(User(**user_in))

    print("SEEDING FOLLOWS")  # Make everyone follow everyone
    for i in range(0, 5):
        for j in range(i, 5):
            if i != j:
                users[i].follow(users[j])

    print("SEEDING PETS")
    pets: List[Pet] = []
    for i in range(0, 5):
        pet_in = {
            "name": f"pet{i}",
            "breed": "Dog",
            "energy": 5,
            "size": "Medium",
        }
        pets.append(Pet(**pet_in))

    print("SEEDING OWNERS")
    for i in range(0, 5):
        for j in range(i, 5):
            pets[i].add_owner(users[j])
