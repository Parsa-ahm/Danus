import time
import threading
import heapq
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass(order=True)
class ScheduledTask:
    run_at: float
    func: Callable = field(compare=False)


class TaskScheduler:
    """Very small task scheduler for deferred actions."""

    def __init__(self):
        self.tasks: List[ScheduledTask] = []
        self.lock = threading.Lock()

    def schedule(self, func: Callable, run_at: float) -> None:
        """Schedule a callable to run at the given Unix timestamp."""
        with self.lock:
            heapq.heappush(self.tasks, ScheduledTask(run_at, func))

    def run_pending(self) -> None:
        """Run all tasks that are due."""
        while True:
            with self.lock:
                if self.tasks and self.tasks[0].run_at <= time.time():
                    task = heapq.heappop(self.tasks)
                else:
                    break
            try:
                task.func()
            except Exception as exc:
                print(f"Task failed: {exc}")

    def run_forever(self, interval: float = 1.0) -> None:
        """Continuously run pending tasks."""
        while True:
            self.run_pending()
            time.sleep(interval)
