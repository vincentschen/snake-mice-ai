# Snake Game with Mice Agent 

## Run 
Run the game with `python game.py`, and pass in options (see below) using the command line. 

For example: `python game.py -s greedy -n 10 -q`
This will run the Greedy snake agent 10 times, with no graphics. 

## Options 
- `-s` or `--snake` (*required*)
  - ['greedy', 'oracle', 'expectimax', 'minimax', 'alphabeta']
- `-n` or `--numGames` (*optional*)
  - Defaults to `numGames = 1`.  
  - [int >= 1]
  - Indicates number of games that should be run to sample over. 
- `-q` or `--quiet` (*optional*)
  - Defaults to `quiet = False`.
  - Flag that indicates whether graphics will be shown.  
- `-d` or `--depth` (*required* for snake = *expectimax* or *minimax* or *alphabeta*)
  - Defaults to `depth = 2`.
  - Indicates depth of search recursion. 
  - [int >= 1]
- `-e` or `--evalFn` (*required* for snake = *expectimax* or *minimax* or *alphabeta*)
  - Indicates which evaluation function is chosen. 
  - ['a', 'b', 'c']