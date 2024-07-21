# adapted from gomoku-thesis-proj
https://github.com/Mig26/gomoku-thesis-proj

I added support for physical boards via webcam. I also optimized a few things. The code for the webcam can be found here. You need to run both programs simultaneously, otherwise, it won't work as expected. The information is transfered via a json file. A file is used to save system resources; a thread is more hardware intensive.  https://github.com/daanvancamp/vijf_op_een_rij_beeldherkenning

A few of the optimizations I have done:

Changed optimizer from Adam to SGD.
Fixed a bug where the training kept repeating the exploration phase: it couldn't choose a move. Now, it is completely random after 30 tries instead of using the function "choose_action". This doesn't have a significant impact on the training process because it happens approximately one in a 1000 times.
The GUI is now more modern.
I also added exception handling in some functions.
2 functions in filereader.py were defined twice, now they are defined just once.
Important:
I added a function in the gomoku class to decrease the learning rate after each training round. By doing so, the model explores more specific patterns. The learning rate is multiplied by 0.9999 after each round, in other words, the learning rate declines by 0,01% after each training round. Like Mikko described in his conclusion: It can improve the performance of the model because the model learns more specific patterns.
I implemented a way to overrule the model. When the opponent has 4 in a row with one open end, then he will never be able to win. When an opponent has 3 in a row with 2 open ends, the function that overrules the model will block this. The model chooses from the list of empty cells. By narrowing down that list, the problem of hallucination is solved with a relatively low amount of computing power. You need a lot af expensive hardware to develop a model that can beat everyone. Overruling can be easily turned on and off by clicking a checkbox in the GUI. Turning it on is recommended, it drastically improves the performance. 

Note: the project is still under development. Some added features aren't stable as of right now.
