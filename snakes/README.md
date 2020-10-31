## Snake
To install run
```bash
pip install -r requirements.txt
```
Model and all 2D coordinates are handled in base/ folder. To run simulation
```bash
python console.py
```
Snake's name and length is shown on the right. When snake dies, it's final length is kept and appended with "-"
### controls for console.py
* q or Esc: quit
* a : to continue simulation automatically
* n : frame by frame execution
### goal
* create a bot that will maximize its length

### current features
* snake will avoid hitting itself or other snakes
* preference towards next cell that has food
* if no moves possible, snake dies and it is converted to food
* periodic boundary conditions
* max number of snakes 26
* each snake is a letter


## Other games to come...