import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

pygame.init()

font = pygame.font.Font('arial.ttf', 25)
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLACK = (0,0,0)

# game settings
BLOCK_SIZE = 50
SPEED = 60

class SnakeGameAI:
    def __init__(self, w=4*BLOCK_SIZE, h=4*BLOCK_SIZE):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('SnakeRL')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                        Point(self.head.x-BLOCK_SIZE, self.head.y),
                        Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def _move(self, action):
        # action array is meant to be representing this: [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        #hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        #hits itself
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        # Draw grid lines
        for x in range(0, self.w, BLOCK_SIZE):
            pygame.draw.line(self.display, WHITE, (x, 0), (x, self.h))
        for y in range(0, self.h, BLOCK_SIZE):
            pygame.draw.line(self.display, WHITE, (0, y), (self.w, y))

        n = len(self.snake)
        for i, pt in enumerate(self.snake):  # Reverse the order of the blocks
            # Calculate the color based on the position of the block in the snake list
            color_intensity = max(0, 255 - i * (255 // n))  # Decrease the intensity for blocks closer to the tail
            block_color = (color_intensity, color_intensity, color_intensity)  # Create a grayscale color with the calculated intensity

            pygame.draw.rect(self.display, block_color, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def play_step(self, action):
        print(f"Frame iteration: {self.frame_iteration}")
        print(f"Snake Size: {len(self.snake)}")
        self.frame_iteration += 1

        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        # move
        self._move(action)
        self.snake.insert(0, self.head)

        # check if game over
        reward = -1  # small penalty for each move
        game_over = False
        death_reason = ''  # initialize death_reason
        if self.is_collision():
            game_over = True
            reward = -20  # large penalty for collision
            death_reason = 'Collision'  # set death_reason to 'Collision'
        elif self.frame_iteration > 5*(len(self.snake)-1):
            game_over = True
            reward = -10  # smaller penalty for timeout
            death_reason = 'Timeout'  # set death_reason to 'Timeout'
        if game_over:
            return reward, game_over, self.score, death_reason  # return death_reason

        # place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 50  # reward for eating food
            self._place_food()
        else:
            self.snake.pop()

        # update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # return game over and score
        print(f"Reward: {reward}")
        return reward, game_over, self.score, death_reason  # return death_reason