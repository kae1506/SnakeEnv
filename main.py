import pygame
import math
import random
import numpy as np

class SnakeEnv():
    WIDTH = 500
    HEIGHT = 500
    ROWS = 50
    TW = WIDTH/ROWS

    def __init__(self, frameRate=10):
        self.frameRate = frameRate
        self.ep_count = 0
        self.step_count = 0
        self.apple_count = 100
        self.render = True

        self.reset()
        

    def randomFood(self):
        food = [random.randint(0, self.ROWS), random.randint(0, self.ROWS)]

        for i in self.snake:
            if i == food:
                return self.randomFood()

        return food

    def Play(self):
        self.reset()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        while True:      
            self.clock.tick(self.frameRate) 
            self.window.fill((0,0,0))

            if self.snake[0][0] in [-1, self.WIDTH/self.TW] or self.snake[0][1]  in [-1, self.HEIGHT/self.TW] or self.snake[0] in self.snake[1:]:
                pygame.quit()
                quit()

            new_head = self.snake[0].copy()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.vel = [0, -1]
                    elif event.key == pygame.K_DOWN:
                        self.vel = [0, 1]
                    elif event.key == pygame.K_LEFT:
                        self.vel = [-1, 0]
                    elif event.key == pygame.K_RIGHT:
                        self.vel = [1, 0]

            new_head[0] += self.vel[0]
            new_head[1] += self.vel[1]
            self.snake.insert(0, new_head)

            #print(food)
            append = True

            for food in self.foods:
                if self.snake[0] == food:
                    self.foods.remove(food)
                    self.foods.append(self.randomFood())
                    append = False
            if append:
                self.snake.pop()

            for cell in self.snake:
                pygame.draw.rect(self.window, (255,255,255), [cell[0]*self.TW, cell[1]*self.TW, self.TW, self.TW])

            for food in self.foods:
                pygame.draw.rect(self.window, (255,0,0), [food[0]*self.TW, food[1]*self.TW, self.TW, self.TW])

            pygame.display.update()

    def reset(self):
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.snake = [
            [25,25],
            [24,25],
            [23,25]
        ]

        self.foods = [self.randomFood() for i in range(self.apple_count)]
        self.done = False
        self.vel = [1,0]

        inputs = []
        inputs.append(self.snake[0][0])
        inputs.append(self.snake[0][1])
        inputs.append(self.vel[0])
        inputs.append(self.vel[1])

        inputs.append(self.findClosest()[0])
        inputs.append(self.findClosest()[1])

        return inputs

    def findClosest(self):
        point = [self.snake[0][0]*self.TW, self.snake[0][1]*self.TW]
        lengths = []
        for pt in self.foods:
            p1 = abs(point[0]-pt[0]*self.TW)*abs(point[0]-pt[0]*self.TW)
            p2 = abs(point[1]-pt[1]*self.TW)*abs(point[1]-pt[1]*self.TW) 
            lengths.append(math.sqrt(p1+p2))

        ind = lengths.index(min(lengths))
        return self.foods[ind]


    def step(self, action):
        reward = 0
        done = False
        if not self.done:
            self.step_count += 1
            if self.ep_count % 15 == 0 and self.ep_count is not 0:
                self.apple_count = self.apple_count - 10 if self.appleCount > 10 else 1
                self.ep_count = 0


            self.window.fill((0,0,0))

            if self.snake[0][0] in [-1, self.WIDTH/self.TW] or self.snake[0][1]  in [-1, self.HEIGHT/self.TW] or self.snake[0] in self.snake[1:]:
                # pygame.quit()
                self.ep_count += 1
                self.reward = -1
                self.done = True
                done = True

            new_head = self.snake[0].copy()
            copy_vel = self.vel
            if action == 0:
                self.vel = [0, -1]
            elif action == 1:
                self.vel = [0, 1]
            elif action == 2:
                self.vel = [-1, 0]
            elif action == 3:
                self.vel = [1, 0]
            elif action == 4:
                self.vel = copy_vel

            new_head[0] += self.vel[0]
            new_head[1] += self.vel[1]
            self.snake.insert(0, new_head)

            #print(food)
            append = True
            for food in self.foods:
                if self.snake[0] == food:
                    self.foods.remove(food)
                    self.foods.append(self.randomFood())
                    append = False
                    reward = 1
            if append:
                self.snake.pop()

            if self.render:
                for cell in self.snake:
                    # counter +=1
                    pygame.draw.rect(self.window, (255,255,255), [cell[0]*self.TW, cell[1]*self.TW, self.TW, self.TW])

                for food in self.foods:
                    if(food == self.findClosest()):
                        pygame.draw.rect(self.window, (0,255,0), [food[0]*self.TW, food[1]*self.TW, self.TW, self.TW])
                    else:
                        pygame.draw.rect(self.window, (255,0,0), [food[0]*self.TW, food[1]*self.TW, self.TW, self.TW])

                pygame.display.update()

                inputs = []
                inputs.append(self.snake[0][0])
                inputs.append(self.snake[0][1])
                inputs.append(self.vel[0])
                inputs.append(self.vel[1])

                inputs.append(self.findClosest()[0])
                inputs.append(self.findClosest()[1])

                return reward, done, inputs



env = SnakeEnv(frameRate=10)
arr = [0,1,2,3,4,4,4,4,4,4,4]
import time
for i in range(10):
    env.reset()
    done = False
    score = 0
    while not done:
        random_ind = random.randint(0, len(arr)-1)
        action = arr[random_ind]
        reward, done, nextState = env.step(action)
        score += reward
        time.sleep(0.25)
    print(score)
# env.Play()
