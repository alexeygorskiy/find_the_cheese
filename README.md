# Find the Cheese!

The goal of this project was to design an environment where a mouse learns to find the cheese. Below are demonstrations of every 10th game (up to game 30):
 
![alt text](https://github.com/alexeygorskiy/find_the_cheese/blob/main/resources/game_0.gif)
![alt text](https://github.com/alexeygorskiy/find_the_cheese/blob/main/resources/game_10.gif)
![alt text](https://github.com/alexeygorskiy/find_the_cheese/blob/main/resources/game_20.gif)
![alt text](https://github.com/alexeygorskiy/find_the_cheese/blob/main/resources/game_30.gif)



## How It Works
This problem is similar to the gridworld problem described in chapter 4 of
[Reinforcement Learning: An Introduction (Second Edition) by Richard S. Sutton and Andrew G. Barto](https://d3c33hcgiwev3.cloudfront.net/Ph9QFZnEEemRfw7JJ0OZYA_808e8e7d9a544e1eb31ad11069d45dc4_RLbook2018.pdf?Expires=1609977600&Signature=JSC5pH44q-us9SeWwlJlfIpb2C3xPNm-zK-O~HzYtEv2uX~VsT5b0nTUDu7G45pIhwHRGAy~BqcJQIS-NwZgxfjsytmdBKib84sOqLUPKs2JX5n-xma8xbX0wYGT6JEP9SVtEe2GE0p~L9lJN7l8Bud2ssy9iTE-BUqjJUtT9wg_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A). The differences are as follows: 
- The agent is given a reward of 300 for entering the terminal state. 
- There is only one terminal state in the bottom right. 
- The gridworld is 48x40 (rows x columns).


The problem is formulated as a finite undiscounted episodic MDP. To add difficulty to the problem the agent can only see at most 2 tiles in any direction and also starts in a random position every time. Every frame the value of all the visible tiles is updated using the value iteration algorithm from chapter 4. As the agent explores the gridworld the value function will eventually converge. Using the greedy policy with respect to the value function, the agent will eventually be able to find the cheese from anywhere using the shortest possible path every time.

An interesting consequence of having a negative reward on every transition in this problem is that in the beginning the agent is motivated to go where it hasn't been before, i.e. explore the gridworld. This is because the longer time it spends in an area, the lower the expected reward will become for those tiles and the agent will move towards unexplored tiles (unexplored tiles have an initiated value of zero).



