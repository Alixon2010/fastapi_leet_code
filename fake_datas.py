import asyncio
from random import choice

import faker

from database import Problem, User


async def fake_problem():
    for i in range(50):
        fake = faker.Faker()
        datas = {
            "name": fake.sentence(nb_words=3),
            "difficulty": choice(list(Problem.Difficulty)),
            "description": fake.paragraph(nb_sentences=3),
        }
        await Problem.create(**datas)


async def main():
    for i in range(50):
        fake = faker.Faker()

        username = fake.user_name()
        firstname = fake.first_name()
        lastname = fake.last_name()
        email = fake.email()
        password = fake.password()
        print(firstname, lastname, email, password)
        await User.create(
            first_name=firstname,
            last_name=lastname,
            email=email,
            password=password,
            username=username,
        )


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(fake_problem())
