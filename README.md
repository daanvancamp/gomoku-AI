# started from gomoku-thesis-proj, but we changed and improved almost everything.
https://github.com/Mig26/gomoku-thesis-proj

**The latest stable release is version 1.4. The recognition doesn't work in this version yet, but all the other features should work perfectly, if not: please report the bug.** That version is the compiled version of the python code. It is made for those who don't want to experience issues caused by features that are in development or those who just want to play it as fast as possible without having to install python or anything else.

stable release:https://github.com/daanvancamp/gomoku-thesis-proj/releases/tag/v1.4

Note: the project is still under development. Some added features aren't stable as of right now, but overall it works better than the program of Mikko (from which I started). The project will hopefully be finished in april of 2025, so you can expect a complete version ultimately then, but it could be done earlier. **The stable version doesn't contain all latest features, but you can download it from the releases tab.** Right now, it is version 1.0. An executable will be released every few weeks.

If you would just clone the repos, then you will most likely experience stability problems or bugs.

I added support for physical boards via webcam, you can easily turn the recogniton via webcam on and off. There's a built-in checkbox for that. It is turned off by default. I also optimized a few things. The code for the webcam can be found here. You need to run both programs simultaneously if you want to use the recognition, otherwise, it won't work as expected. The data is transfered via a json file. A file is used to save system resources; a thread puts more strain on the hardware. A constant connection with the webcam is also recommended because it takes about 5 seconds to connect to the webcam. The program should run perfectly fine on a relatively low-spec computer. 
https://github.com/daanvancamp/five_in_a_row_recognition
The usage of the recognition feature can be controlled via a checkbox.
We are working on integrating the two programs. We will integrate them when the recognition is stable and functional.


I also want to mention the following: "please don't hesitate to report any bugs". There are probably many undiscovered bugs. Please check if your bug if listed below before reporting it, because then it's a known issue/bug. Feature suggestions are also more than welcome, because they can help to develop a better, more versatile program. **Don't report any bugs in the code in this repository. Only report bugs that were caused by the executable file.**

A few of the optimizations I have done and some added features:


These improvements are more extensively described in the commits, read them if you want to know the improvements/solutions in detail. Some small improvements/solutions are left out below.

June 2024:

  started adding support for webcams
  
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

  The code was completely restructured. There are now 3 functions to run the game.

  **You can now choose if you want to allow overruling for each player. Of course, I also added an option in the GUI.**
  **All the options that you can't choose because that would cause a crash are now hidden.**
  
  splitted the run game function into 3 functions: runreplay, rungame,runtraining

  **released version 0.1**

  added an option in the GUI to turn the music on and off.
  
  added common code to functions to shorten the code (gomoku.py went from 900 to 700 lines)
  
  **fixed an issue: Like you see on the image. It's the turn of Black.
  ![image](https://github.com/user-attachments/assets/46c63a9a-af7f-4f0a-9cf3-2bf9f56af9ac) 
  
  You could always win when you started from the ends and made your way to the middle. The model sometimes didn't block it. It turned out that it was the result of a small bug in the overruling.**
  
  fixed a few general bugs

  **big performance and stability improvements, the GUI won't crash anymore. If it does, please report that.** There was no event loop when there was no Human in the game. So one click would cause the GUI to crash.
  
  **released version 1.0**

  fixed some crash issues and bugs

  buttons and labels are now grayed out instead of invisible

  restructured code, added class to save model stats: new module

  added more stats to tab 4

  rewrited modelmanager class

  
  **released version 1.1**

  added even more stats in the models tab

  fixed a crash issue where the program would crash after deleting a model

  fixed other bugs and crash issues

  **released version 1.2**


  embedded the pygame window into a bigger, fullscreen tkinter window that shows all necessary information

  **released version 1.3**


  added an option in the GUI so you can now choose if you want to see graphs after training the model

  stability improvements & bugfixes

  visual improvements in the small GUI

  cleaned up code

  solved an issue  where the fullscreen GUI would flicker

  You can now safely exit the fullscreen GUI by pressing escape.


  **released version 1.4**
  
  first implementation of the integrated recognition

  restructured, the fullscreen GUI and the recognition are now each part of their own module.


**issues:**

You shouldn't experience any issues at the moment.


**roadmap(in descending priority):**

-We are currently working on integrating the two programs.

-coming soon, but it's done as of right now.



developped by:
daanvancamp & wimnevelsteen
