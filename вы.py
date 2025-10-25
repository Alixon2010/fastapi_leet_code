import asyncio

from database import User, Problem, Topic, Language, Submission, Example

examples_data = [
]





if __name__ == "__main__":
    async def f():
        for user in examples_data:
            await Example.create(**user)


    asyncio.run(f())