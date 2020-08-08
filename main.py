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
                # print(self.snake, food)
                if self.snake[0] == food:
                    self.foods.remove(food)
                    self.foods.append(self.randomFood())
                    append = False
            if append:
                self.snake.pop()

                # print(snake)

                # sn = []
                # for i in range(len(snake)):
                #     sn.append(snake[len(snake)-1-i])
                # counter = 0
            for cell in self.snake:
                # counter +=1
                pygame.draw.rect(self.window, (255,255,255), [cell[0]*self.TW, cell[1]*self.TW, self.TW, self.TW])

            for food in self.foods:
                pygame.draw.rect(self.window, (255,0,0), [food[0]*self.TW, food[1]*self.TW, self.TW, self.TW])

            pygame.display.update()

    def findDistances(self, angle):
        walls = []
        point = [self.snake[0][0]*self.TW, self.snake[0][1]*self.TW]
        for food in self.foods:
            i = food[0]*self.TW
            j = food[1]*self.TW

            wall1 = [[i   , j   ], [i   , j+self.TW]]
            wall2 = [[i   , j   ], [i+self.TW, j   ]]
            wall3 = [[i+self.TW, j+self.TW], [i+self.TW, j   ]]
            wall4 = [[i+self.TW, j+self.TW], [i   , j+self.TW]]
            walls.append(wall1)
            walls.append(wall2)
            walls.append(wall3)
            walls.append(wall4)

        for wall in walls:
            pt = self.rayCast(wall, angle)
            if(pt):
                pygame.draw.line(self.window, (255,255,255), point, pt)
                pygame.display.update()
                p1 = abs(point[0]-pt[0])*abs(point[0]-pt[0])
                p2 = abs(point[1]-pt[1])*abs(point[1]-pt[1]) 
                return math.sqrt(p1+p2)
            else:
                return 0
                

    def rayCast(self, wall, angle):
        angles = np.array([np.cos(angle), np.sin(angle)])

        x1 = wall[0][0]
        y1 = wall[0][1]
        x2 = wall[1][0]
        y2 = wall[1][1]

        x3 = self.snake[0][0]*self.TW
        y3 = self.snake[0][1]*self.TW
        x4 = self.snake[0][0]*self.TW + angles[0]
        y4 = self.snake[0][1]*self.TW + angles[1]

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if (den == 0):
            return None
    

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if (t > 0 and t < 1 and u > 0):
            pt = np.array([0,0])
            pt[0] = 1 + t * (x2 - x1)
            pt[1] = y1 + t * (y2 - y1)
            return pt
        else:
            return None
        
    

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
                self.apple_count -= 20
                self.ep_count = 0


            self.window.fill((0,0,0))

            if self.snake[0][0] in [-1, self.WIDTH/self.TW] or self.snake[0][1]  in [-1, self.HEIGHT/self.TW] or self.snake[0] in self.snake[1:]:
                # pygame.quit()
                self.ep_count += 1
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
    print("gotting")
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