class Future:
    def __init__(self):
        self.done = False
        self.result = None
    
    def __await__(self):
        while not self.done:
            print("Future is yielding control to the event loop")
            k = yield   # Yield control to the event loop. Also shows that a value can be passed back to the coroutine when it is resumed by the event loop. This is just to demonstrate that the event loop can send values back to the coroutine when it resumes it.
            print("Future received value from event loop:", k)
        return self.result # Return the result when the future is done. This will be the value that is returned by the await expression in the coroutine that is awaiting this future.
        print("Future is done")
    
    def set_result(self,result):
        self.result = result
        self.done = True

async def helloA(fut):
    print("Starting hello A")
    val = await fut
    print("Finished hello with result:", val)

async def helloB(fut):
    print("Starting hello B")
    val = await fut
    print("Finished hello with result:", val)

def run():
    print("Starting someRoutine")
    futA = Future()
    futB = Future()
    items = [(helloA(futA),futA,2), (helloB(futB),futB,2)] # List of tuples of coroutine, future and the number of iterations to run before setting the result of the future. This is just to simulate some work being done in the coroutines before they set the result of the future.
    while items:
        coro, fut, iter = items.pop(0)
        try:
            print("Running coroutine...", coro)
            coro.send(None) if iter == 2 else coro.send("Hello from event loop") # Start the coroutine by sending None. If iter is 1, send a value to the coroutine to simulate some work being done in the coroutine before it sets the result of the future.
            iter -= 1
            if not iter:
                fut.set_result(("Hello from Future", fut))
                print("Future result set:", fut.result)
            print("Coroutine yielded control back to the event loop\n")
            items.append((coro, fut, iter))
        except StopIteration as e:
            print("Last value from awaitable received:", e.value)
            print("")
    print("Result from A:", futA.result)
    print("Result from B:", futB.result)

run()

"""
Output:
% python3.14 future.py                                      
Starting someRoutine
Running coroutine... <coroutine object helloA at 0x100e3cd40>
Starting hello A
Future is yeilding control to the event loop
Coroutine yielded control back to the event loop

Running coroutine... <coroutine object helloB at 0x100f4de50>
Starting hello B
Future is yeilding control to the event loop
Coroutine yielded control back to the event loop

Running coroutine... <coroutine object helloA at 0x100e3cd40>
Future received value from event loop: Hello from event loop
Future is yeilding control to the event loop
Future result set: ('Hello from Future', <__main__.Future object at 0x100eba120>)
Coroutine yielded control back to the event loop

Running coroutine... <coroutine object helloB at 0x100f4de50>
Future received value from event loop: Hello from event loop
Future is yeilding control to the event loop
Future result set: ('Hello from Future', <__main__.Future object at 0x100ea7250>)
Coroutine yielded control back to the event loop

Running coroutine... <coroutine object helloA at 0x100e3cd40>
Future received value from event loop: Hello from event loop
Future is done
Finished hello with result: ('Hello from Future', <__main__.Future object at 0x100eba120>)
Last value from awaitable received: None

Running coroutine... <coroutine object helloB at 0x100f4de50>
Future received value from event loop: Hello from event loop
Future is done
Finished hello with result: ('Hello from Future', <__main__.Future object at 0x100ea7250>)
Last value from awaitable received: None

Result from A: ('Hello from Future', <__main__.Future object at 0x100eba120>)
Result from B: ('Hello from Future', <__main__.Future object at 0x100ea7250>)
"""