# adapted from gomoku-thesis-proj
https://github.com/Mig26/gomoku-thesis-proj
I added support for physical boards via webcam. I also optimized a few things.

a few optimizations I have done:
changed optimizer from Adam to SGD
fixed a bug where the training kept repeating the exploration fase: It couldn't choose a move. Now, it is completely random after 30 try's.

