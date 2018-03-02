# Baroque Chess Player

This project, created by Aaron Bae and Daniel Short, contains an AI that plays
the game of Baroque Chess. It uses alpha-beta pruning to make move decisions
along with Zobrist hashing to speed up the process.  

## Approach

Our approach will be to first understand the rules,
then code our move generator, develop a static evaluation function,
a personality for the agent, and then optimize using alpha-beta
pruning, Zobrist hashing, and comparison of alternative static
evaluation functions.

## References

Please read [Wikipedia article on Baroque Chess](https://en.wikipedia.org/wiki/Baroque_chess) for details on how the game of Baroque Chess is played. Also, read [Wrong with Ultima](http://www.logicmazes.com/games/wgr.html) if you're interested in what
Robert Abbott the creator of the game had to say about this game.

## Authors

* **Aaron Bae** - *static evaluation function*
* **Daniel Short** - *optimizations of alpha-beta pruning and Zobrist hashing*


## Acknowledgments

* Thanks to UW CSE415 for giving us an opportunity to create this project
* Steve Tanimoto Ph.D
