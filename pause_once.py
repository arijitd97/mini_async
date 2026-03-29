
class PauseOnce:
    def __init__(self):
        pass
    def __await__(self):
        print("Hello From PauseOnce")
        yield # Suspends the execution of the __await__ method and returns control to the first most caller(Here coro.send(None)).
        print("Resuming from PauseOnce")


async def temp(): # Example coroutine function. This do not yield to the event loop
    return
    
# Coroutine A
async def helloA():
    po = PauseOnce()
    print("1. Hello A!")
    #await temp() # This doesn't work as expected as temp does not have a suspension point like __await__ in po.
    await po
    print("2. Hello A!")
    await po
    print("3. Hello A!")

# Coroutine B
async def helloB(po = PauseOnce()):
    print("1. Hello B!")
    await po
    print("2. Hello B!")
    await po
    print("3. Hello B!")

# Simple eventloop to run coroutines in a round-robin fashion until they are done.
def run():
    items = [helloA(), helloB()]
    while items:
        coro = items.pop(0)
        try:
            print(coro.send(None)) # Start or resume the coroutine. If the coroutine yields, it will be suspended and control will return to this loop. If the coroutine raises StopIteration, it means it has finished execution and we can ignore it.
            items.append(coro)
        except StopIteration as e:
            print(e.value)


run()

"""
Output:
% python3.14 pause_once.py
1. Hello A!
Hello From PauseOnce
None                # yield returns None to the caller of __await__ method which is the await expression in helloA. The execution of helloA is suspended until the next call to send().
1. Hello B!
Hello From PauseOnce
None
Resuming from PauseOnce
2. Hello A!
Hello From PauseOnce
None
Resuming from PauseOnce
2. Hello B!
Hello From PauseOnce
None
Resuming from PauseOnce
3. Hello A!
None
Resuming from PauseOnce
3. Hello B!
None
"""