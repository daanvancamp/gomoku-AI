# adapted from gomoku-thesis-proj
https://github.com/Mig26/gomoku-thesis-proj

I added support for physical boards via webcam. I also optimized a few things.

A few of the optimizations I have done:

Changed optimizer from Adam to SGD.
Fixed a bug where the training kept repeating the exploration phase: it couldn't choose a move. Now, it is completely random after 30 tries instead of using the function "choose_action". This doesn't have a significant impact on the training process because it happens approximately one in a 1000 times.
Important:
I added a function in the gomoku class to decrease the learning rate after each training round. By doing so, the model explores more specific patterns. The learning rate is multiplied by 0.9999 after each round. Like Mikko described in his conclusion: It can improve the performance of the model because the model learns more specific patterns.
The GUI is now more modern.

Note: it is still under development. The added features aren't stable as of right now.

