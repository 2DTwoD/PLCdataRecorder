import sched
import time

from misc.types import MutableBool


#Не используется, sched.scheduler.run() - блокирует поток без возможности отмены
class Repeat(sched.scheduler):
    def __init__(self, period, action, in_process: MutableBool = None):
        super().__init__(time.monotonic, time.sleep)
        self._period = period
        self._action = action
        self._in_process = in_process
        self._event = None

    def _go(self):
        if self._in_process.get():
            self._event = self.enter(self._period, 1, self._go)
            self._action()

    def start(self):
        if self._in_process is not None:
            self._event = self.enter(0, 1, self._go)
            self.run()

    def stop(self):
        if not self.empty():
            self.cancel(self._event)
