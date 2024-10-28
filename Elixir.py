import time
from threading import Thread


class Elixir:
    maxValue = 10.0

    def task(self):
        while not self.canStop:
            time.sleep(2.8)
            if self.value < self.maxValue:
                self.value = self.value + 1.0
                # print(f'value: {self.value}\n')
                # ElixirDisplay(self.pos, self.groups, self.value)

    def __init__(self):
        self.canStop = False
        self.value = 0.0
        self.thread = Thread(target=self.task)
        self.thread.start()

    def __str__(self):
        return f'{self.value}'

    def stop(self):
        self.canStop = True


if __name__ == "__main__":
    e = Elixir()
    c = 0;

    while c < 10:
        print(e.value)
        time.sleep(3)
        c = c +1

    e.value = 3.0

    c= 0
    while c < 10:
        print(e.value)
        time.sleep(3)
        c = c + 1

    e.canStop = True
    e.thread.join
    print("joined the thread and stopped ")
