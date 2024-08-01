import pygame
import random


class Environment:
  def __init__(self):
    pygame.init()
    self.block_size = 30
    self.grid_size = (5, 5)
    self.screen_size = (self.grid_size[0] * self.block_size, self.grid_size[1] * self.block_size)
    self.screen = pygame.display.set_mode(self.screen_size)
    self.clock = pygame.time.Clock()
    self.snake_assets = {
      "head": pygame.image.load("./assets/head.png"),
      "straightBody": pygame.image.load("./assets/straightBody.png"),
      "bendBody": pygame.image.load("./assets/rightUpBody.png"),
      "tail": pygame.image.load("./assets/tail.png")
    }
    self.food_asset = pygame.image.load("./assets/food.png")
    self.score = 0
    self.snake = [(2, 2), (1, 2), (0, 2)]
    self.food = self.place_food()
    self.direction = (1, 0)

  def place_food(self):
    while True:
      x = random.randint(0, self.grid_size[0] - 1)
      y = random.randint(0, self.grid_size[1] - 1)
      if (x, y) not in self.snake:
        return (x, y)

  def draw_grid(self):
    for x in range(0, self.screen_size[0], self.block_size):
      for y in range(0, self.screen_size[1], self.block_size):
        rect = pygame.Rect(x, y, self.block_size, self.block_size)
        color = (0, 100, 0) if (x // self.block_size + y // self.block_size) % 2 == 0 else (0, 200, 0)
        pygame.draw.rect(self.screen, color, rect)

  def update_snake(self):
    head = self.snake[0]
    new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
    self.snake.insert(0, new_head)
    self.snake.pop()

  def draw_snake(self):
    for i, segment in enumerate(self.snake):
      asset = self.snake_assets["straightBody"]
      if i == 0:
        asset = self.snake_assets["head"]
        asset = pygame.transform.rotate(asset, self.get_rotation_angle(i))
      elif i == len(self.snake) - 1:
        asset = self.snake_assets["tail"]
      else:
        if self.is_bending(i):
          asset = self.snake_assets["bendBody"]
          asset = pygame.transform.rotate(asset, self.get_rotation_angle(i))
      self.screen.blit(asset, (segment[0] * self.block_size, segment[1] * self.block_size))

  def get_rotation_angle(self, i):
    # calculate rotation angle based on direction
    if self.direction == (1, 0):  # moving right
      return 0
    elif self.direction == (0, 1):  # moving down
      return 90
    elif self.direction == (-1, 0):  # moving left
      return 180
    elif self.direction == (0, -1):  # moving up
      return 270

  def is_bending(self, i):
    # check if the snake is bending at segment i
    pass

  def draw_food(self):
    self.screen.blit(self.food_asset, (self.food[0] * self.block_size, self.food[1] * self.block_size))

  def update(self):
    self.screen.fill((0, 0, 0))
    self.draw_grid()
    self.update_snake()
    self.draw_snake()
    self.draw_food()
    pygame.display.flip()
    self.clock.tick(10)

  def run(self):
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
            self.direction = (0, -1)
          elif event.key == pygame.K_DOWN:
            self.direction = (0, 1)
          elif event.key == pygame.K_LEFT:
            self.direction = (-1, 0)
          elif event.key == pygame.K_RIGHT:
            self.direction = (1, 0)
      self.update()
    pygame.quit()

if __name__ == "__main__":
  env = Environment()
  env.run()