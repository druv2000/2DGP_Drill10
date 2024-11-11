from random import random

from pico2d import load_image, get_time

import game_framework
from boy import Idle
from state_machine import StateMachine, bird_start_run, bird_stop_run

# run speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAME_PER_ACTION = 14

class BirdIdle:
    @staticmethod
    def enter(bird, e):
        bird.dir = 1
        bird.frame = 0
        bird.sprite_line = 0
        bird.wait_time = get_time()

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if not bird.state_machine.event_que:
            bird.state_machine.add_event(('BIRD_START_RUN', 0))

    @staticmethod
    def draw(bird):
        bird.image.clip_draw(int(bird.frame) * 100, bird.action * 100, 100, 100, bird.x, bird.y)

class BirdRun:
    @staticmethod
    def enter(bird, e):
        bird.frame = 0
        bird.sprite_line = 0
        pass

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAME_PER_ACTION
        print(f'bird_frame: {bird.frame}')
        if bird.frame < 5:
           bird.sprite_line = 0
        elif bird.frame < 10:
            bird.sprite_line = 1
        else:
            bird.sprite_line = 2

        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time


    @staticmethod
    def draw(bird):
        bird.image.clip_draw(int(bird.frame) * 183, bird.sprite_line * 168, 183, 168, bird.x, bird.y)

class Bird:

    def __init__(self, x = 400, y = 300):
        self.x, self.y = x, y
        self.face_dir = 1
        self.image = load_image('bird_animation.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(BirdIdle)
        self.state_machine.set_transitions(
            {
                BirdIdle: {bird_start_run: BirdRun},
                BirdRun: {bird_stop_run: BirdIdle},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()