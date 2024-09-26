from typing import Callable, TypeVar
from queue import Queue
from threading import Thread

def queuefy(target: Callable, while_trigger: Callable, args = ()):
    q = Queue()
    def fn(q: Queue):
        while while_trigger():
            q.put(target(*args))
    thread = Thread(target=fn, args=[q], daemon=True)
    thread.start()
    return q
