### Bifurcation

Simple game that you play interactively with the computer.
You can run it locally - the only thing needed is stdin and stdout.

It includes a simple tutorial so you can learn how to move in the game.

The flag is encoded in a binary tree.
Each level includes two letters and the position of the player.
You need to move the player to one of the exits.
When you do that, you collect a letter that was on the exit. Find all of the letters and you get the flag.
Only one path through the tree ends with "}" - that's the flag.

In flag.py there are functions for writing the flag down to the tree and generating random other branches.

It takes 2**len(flag) of attempts to brute it, so realistaically each character after ~10 is making it a lot harder to solve over the internet.

Each game is played from scratch, so once you see both letters from the level you need to start another connection and get to the same place you are right now in order to pick a different path.

The goal of the challange is to figure out the automation of this process – which is pretty simple and straightforward.

See local_solver.py for an example how to solve it with subprocess by interacting with stdin and stdout.
