# Team-Segfault

Team members:

- [Vuk Đorđević](https://github.com/MegatronJeremy)
- [Ricardo Suarez del Valle](https://github.com/RicardoSdV)
- [Jovan Milanović](https://github.com/wanjoh)

### Game description

The game can have bot players, remote players, and observers.
It is a turn-based strategy game played on a hexagonal map, with each player being assigned five different tanks.
Each game is uniquely identified by its name, and the same goes for each player joining that game.
When starting the game you will be greeted by a menu screen where you can change the game configuration as you wish.
After starting the game and waiting for all the players to join, a simulation will play out in which the different
players will battle each other, until the game ends in a draw or a winner is determined.

### Running

Set the project workspace to the folder which contains main.py, call wanted tests inside of the main function and run
the module.
For testing remote games run the remote_game_create and remote_game_join modules separately, with the same project
configurations as for the previously
named.
Python 3.11 <= is required.

### Project structure

A simplified version of the project structure can be seen here:
![VLLDZZ~1](https://user-images.githubusercontent.com/81580576/235317295-928da99f-785b-4219-a8fc-f8f0fe809311.PNG)

The DisplayManager is the top-level entry point of the program, but the Game class can be run and configured itself
without it, in which case no window will be rendered, and only console output can be seen.

### Assets

[Tank classes icons](https://icon-library.com/icon/world-of-tanks-icon-12.html)

[Tank icon](https://www.freeiconspng.com/img/19109)

[Explosion](https://www.pngwing.com/en/free-png-xiyem)

[Explosion sound](https://pixabay.com/sound-effects/explosion-6055/)

[Gunshot sound](https://pixabay.com/sound-effects/shotgun-firing-3-14483/)

[Projectile](https://www.freepnglogos.com/images/bullet-8545.html)

[Tank icon for pygame window](https://www.flaticon.com/free-icon/tank_3111508)

[Tank tracks](https://www.dreamstime.com/tank-tracks-set-track-treads-isolated-white-various-caterpillar-impressed-heavy-vehicles-like-tractors-bulldozers-image198577121)

[Catapult image](https://opengameart.org/content/catapult-1)