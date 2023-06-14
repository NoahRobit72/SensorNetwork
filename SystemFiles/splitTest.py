import asyncio

async def loop1():
    while True:
        print("hi mom")
        await asyncio.sleep(.001)  # Add a sleep to avoid blocking the event loop

async def loop2():
    while True:
        print("hi dad")
        await asyncio.sleep(.001)  # Add a sleep to avoid blocking the event loop

# Create and run the coroutines concurrently
async def main():
    await asyncio.gather(loop1(), loop2())

asyncio.run(main())