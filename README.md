# SnakeEnv
This is my attempt at creating a Snake Environment For Reinforcement Learning, similar to those in OpenAI's gym.
Please do read this, as this is my first attempt at making a environment, and i may have done things a little different.

 
# How to make it work
Although its as simplified as i can get it, i will provide some information about how it works, and how you can use it

For simplicity purposes, you will have to pass in an argument in the environment called frameRate. This will be the spped of the game if u choose to pay it yourself.

There are two main functions- env.Play(), env.step()
env.Play() allows you to play with the arrow keys.

env.step() works quite like OpenAI's gym environments. Its returns: rewards, done, nextState.

The reward function is quite basic. It give a reward of +1 when it gets an apple, 0 when it doesnt.
To overcome the sparse reward situation with this reward function, I have added 100 apples in the beginning.
As the episodes continue, it slowly decreases to one.

The input is a vector of 6 values, and theree are 5 possible actions.
Inputs - x, y of the head of the snake
         xVelocity, yVelocity of the snake
         x, y, of the closest apple
         
Actions - 0-Up
          1-Down
          2-Left
          3-Right
          4-Do Nothing.
          
The game is only over when either the snake hits the walls, or hits itself.

Rendering is inbuilt and enabled by default. No function is required, but there is a attribute (env.render) which can be set to False 
if rendering is not preferred.

One Nuance which i would like to point out is that if u are rendering, then i suggest after each step, you add time.sleep(0.25). This will give a realistic 
speed for watching.

I have set a random agent playing ten episodes in the environment.
