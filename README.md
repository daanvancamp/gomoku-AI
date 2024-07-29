# adapted from gomoku-thesis-proj
https://github.com/Mig26/gomoku-thesis-proj

I added support for physical boards via webcam, you can easily turn the recogniton via webcam on and off. There's a built-in checkbox fot that. It is turned off by default. I also optimized a few things. The code for the webcam can be found here. You need to run both programs simultaneously if you want to use the recognition, otherwise, it won't work as expected. The data is transfered via a json file. A file is used to save system resources; a thread puts more strain on the hardware. A constant connection with the webcam is also recommended because it takes about 5 seconds to connect to the webcam. The program should run perfectly fine on a relatively low-spec computer. https://github.com/daanvancamp/vijf_op_een_rij_beeldherkenning The usage of the recognition feature can be controlled via a checkbox.
We are working on integrating the two programs. We will integhrate them when they are both stable.

I also want to mention the following: "please don't hesitate to report any bugs". There are probably many undiscovered bugs. Please check if your bug if listed below before reporting it, because then it's a known issue/bug. Feature suggestions are also more than welcome, because they can help to develop a better, versatile program.

A few of the optimizations I have done and some added features:


These improvements are more extensively described in the commits, read them if you want to know the improvements/solutions in detail. Some small improvements/solutions are left out below.

June 2024:

  added support for webcams
  
july 2024:

  **Changed the optimizer of the neural networkfrom Adam to SGD.**
  
  **Fixed a bug where the training kept repeating the exploration phase: it couldn't choose a move. Now, it is completely random after 30 tries instead of using the function "choose_action". This doesn't have a significant         impact on the training process because it happens approximately one in a 1000 times.**
  
  The GUI is now more modern and looks better than ever/before.
  
  I also added exception handling in some functions. The involved functions are now more stable.
  
  2 functions in filereader.py were defined twice, now they are defined just once. That's a small error of Mikko.
  
  **I added a function in the gomoku class to decrease the learning rate after each training round. By doing so, the model explores more specific patterns. The learning rate is multiplied by 0.9999 after each round, in other       words, the learning rate declines by 0,01% after each training round. Like Mikko described in the conclusion of his thesis : It can improve the performance of the model because the model learns more specific patterns.**
  
  **I implemented a way to overrule the model. When the opponent has 4 in a row with one open end, then he will never be able to win. When an opponent has 3 in a row with 2 open ends, the function that overrules the model will     
  block this. The model chooses from the list of empty cells. By narrowing down that list, the problem of hallucination is solved with a relatively low amount of computing power. You need a lot af expensive hardware to develop a   model that can beat everyone. Overruling can be easily turned on and off by clicking a checkbox in the GUI. Turning it on is recommended, it drastically improves the performance. The choices are explained in the terminal and     saved to a textfile along with the board, so you can reread the reasons why the program performs a certain action. This is important because some moves can seam weird to a human, although there are a few bugs.**
  
  I added an on-screen hover effect when the mouse hovers over the board to make it look better and to prevent misclicks.
  
  I added a checkbox to train the model against yourself. (human vs DVC-AI) My name is Daan Van Camp, so my initials are DVC.
  
  Wim added a way to load a situation and load from there, so it's easier to find the weaknesses of the model.
  
  The last move of the model is now red so it's easier to find the last move and anticipate upon it.
  
  Human training checkbox has now moved to a more appropriate place.
  
  **You can now train multiple models using this program.**
  
  There's now a checkbox in the GUI so you can easily turn the recognition on and off.
  
  Loading a situation is now integrated into the play game tab.
  
  The "global" variables aren't stored in files anymore, now they really are global variables.

  I added more test situation, so the performance of the model can be tested more extensively and the overruling/training can be optimized.
  
  
  august 2024:

  ...
  
  

issues:

There's a known issue/weakness. Like you see on the image. It's the turn of Black.
![image](https://github.com/user-attachments/assets/46c63a9a-af7f-4f0a-9cf3-2bf9f56af9ac) 
You can always win when you start from the ends and make your way to the middle. The model sometimes won't block it, but no one plays like that. If a 100 people (who have never played the game) would play the game, then they all wouldn't find out about this bug. Someone who knows all the existing bugs and vulnerabilities (and takes 30 seconds to think about each move), will never lose against the model.

roadmap:

-We are trying to make using multiple models more stable.

-I am further developping the feature to turn the recognition on and off.

-solving the issues mentioned above, including the issue with the overruling

-We are working on integrating the two programs. We will integrate them when they are both stable.

-coming soon


Note: the project is still under development. Some added features aren't stable as of right now, but overall it works better than the program of Mikko (from which I started). The project will hopefully be finished in april of 2025, so you can expect the stable and complete version ultimately then, but it could be done earlier.

developped by:
daanvancamp & wimnevelsteen
