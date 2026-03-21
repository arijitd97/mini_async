
import asyncio


async def hello():
    print("Hello!")
    return "Hello again!"



async def main():
    # Coroutine object is created but not awaited(execution paused)
    r = hello()
    print("Before sending:", r)
    try:
        # The first call to send() starts the coroutine.
        k = r.send(None)
        print("This",k,type(k)) # Never printed becaue the coroutine throws StopIteration.
    except StopIteration as e:
        print(e.value) # Hello again! is printed as the return value of the coroutine.
    


if __name__ == "__main__":
    asyncio.run(main())