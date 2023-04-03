# Team-Segfault

### Game description

The game can have human, bot players, and observers. It is played on a hexagonal map with a certain number of turns. The game class manages the game state, initializes the players and client connections, runs the game in a loop.
The game currently supports one (for a single-player game), or more (for a multiplayer game) trivial bots playing together.

### Running

Set the project workspace to the folder which contains main.py, call wanted tests inside of the main function and run the module.

### Troubleshooting

If map drawing is not working and error ```UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.``` occurs on Debian based systems, 
you need to install tkinter with ```sudo apt-get install python3-tk``` or install any of the matplotlib supported GUI backends.
