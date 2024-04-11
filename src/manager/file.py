# python imports
from math import ceil

# project imports
from manager import Manager


class FileOutput(Manager):
    def __init__(self, dt=0.1, output_file='out.csv', simulation_time=30, **config):
        super().__init__(dt=dt, **config)

        self.iter = reversed(range(int(ceil(simulation_time / dt))))
        self.file = open(output_file, "w")
        self.file.write(f'x,theta' + "\n")

    def resume(self):
        return next(self.iter)

    def draw(self, world):
        self.file.write(f'{world.x},{world.theta}' + "\n")

    def wait(self):
        pass

    def quit(self):
        self.file.close()
