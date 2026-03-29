import time
from collections import deque
import heapq

class Future:
    def __init__(self):
        self.done = False
        self.result = None
        self.callbacks = []  # List of callbacks to call when the future is done

    def set_result(self, result):
        self.result = result
        self.done = True
        print("Future result set")
        for callback in self.callbacks:
            print("Calling callback from future", callback)
            callback(self)

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def __await__(self):
        while not self.done:
            print("Future is yielding self")
            yield self
        print("Future is done, returning result")
        return self.result
    
class Task:
    def __init__(self, coro, loop, future=None, name=None):
        self.coro=coro
        self.loop=loop
        self.future=future
        self.name=name
        self.result=None

    def step(self, value=None):
        try:
            fut = self.coro.send(value)
            print(f"Task {self.name} yielded future: {fut}")
            fut.add_callback(self._wakeup)
            print("Added callback to future for task:", self.name)
            print()
        except StopIteration as e:
            self.result = e.value
            print(f"Task {self.name} completed with result: {self.result}")
            print()

    def _wakeup(self, fut):
        print(f"Waking up task: {self.name}")
        self.loop.schedule(self, fut.result)
    


class Loop:
    # Event Loop that manages scheduled tasks and waiting futures
    def __init__(self):
        self.tasks = deque()  # Queue of scheduled tasks (coroutines)
        self.waiting = []     # Min-heap of waiting futures (time, future)

    def create_task(self, coro, future=None, name=None):
        task = Task(coro, self, future=future, name=name)
        print("Creating task:", name, "with coroutine:", coro)
        self.schedule(task)
        return task

    def schedule(self,task,value=None):
        self.tasks.append((task, value))

    def call_later(self, delay, fut):
        calltime = time.time() + delay
        heapq.heappush(self.waiting, (calltime, fut))
    
    def run(self):
        while self.tasks or self.waiting:
            now = time.time()
            while self.waiting and self.waiting[0][0]<=now:
                print("Time to wake up a future!")
                _, fut = heapq.heappop(self.waiting)
                fut.set_result(None)
            
            if self.tasks:
                task, value = self.tasks.popleft()
                print("Running task:", task.name)
                task.step(value)
            else:
                print("No tasks to run, sleeping for a bit...")
                time.sleep(0.1)

loop = Loop()
async def sleep(duration):
    print(f"Sleeping for {duration} seconds...")
    now = time.time()
    fut = Future()
    loop.call_later(duration, fut)
    await fut
    print(f"Woke up after {time.time()-now} seconds!")

async def worker(delay, name):
    print(f"Worker {name} starting")
    await sleep(delay)
    print(f"Worker {name} done")

async def loop_hogger():
    print(f"Loop Hogger starting")
    time.sleep(6)
    print(f"Loop Hogger done")

loop.create_task(coro=worker(4,"A"), name="A")
loop.create_task(coro=loop_hogger(), name="Loop Hogger")
loop.create_task(coro=worker(2,"B"), name="B")
loop.run()






"""
“The loop schedules tasks.”
“Tasks drive coroutines.”
“Tasks suspend on futures.”
“Future completion wakes the task.”
"""

"""
Your homemade sleep() should:

create a future
tell the loop, “wake this up later”
pause the task until that time
"""

"""
Step 8: Final demo
Create final_demo.py.

Make something small and readable, like:

cooking steps
homework tasks
coffee shop orders
a mini job runner
Example:

async def make_toast():
    print("Toast: start")
    await sleep(1)
    print("Toast: done")

async def boil_water():
    print("Water: start")
    await sleep(0.5)
    print("Water: done")
Run 2 or 3 of them together.

This final demo should show:

multiple tasks start
they pause with await sleep(...)
the loop resumes them later
"""