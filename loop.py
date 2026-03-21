# A simple implementation of an event loop to run a coroutine
def run(coro):
    try:
        while True:
            print("Running coroutine...")
            coro.send(None) # Start the coroutine by sending None
    except StopIteration as e: # The coroutine has finished execution and raises StopIteration with the return value
        return e.value # The return value of the coroutine
    
# Define a simple coroutine that prints a message and returns a value
async def hello():
    print("Hello!")
    return "Hello again!"


coro = hello() # Create a coroutine object by calling the async function. The coroutine is not executed yet.
result = run(coro) # Send the coroutine to the event loop to run it. The result is the return value of the coroutine.
print(result)
