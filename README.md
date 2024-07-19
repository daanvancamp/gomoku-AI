# adapted from gomoku-thesis-proj
https://github.com/Mig26/gomoku-thesis-proj
I added support for physical boards via webcam. I also optimized a few things.

A few of the optimizations I have done:

Changed optimizer from Adam to SGD.
Fixed a bug where the training kept repeating the exploration phase: it couldn't choose a move. Now, it is completely random after 30 tries instead of using the function. This doesn't have a significant impact on the training process because it happens approximately one in a 1000 times.

Note: it is still under development. The added features aren't stable.

