# Gomoku-AI
I added support for physical boards via webcam. I also optimized a few things. The code for the recognition can be found here, but it is already built in and has been updated. The outdated recognition code can be found here:
https://github.com/daanvancamp/five_in_a_row_recognition

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
  
  added folders to the repository

  visual improvements in the game window

  The mainmenu is now fullscreen and integrated with the gamewindow.

  You can now acces all "tabs" by using the menubar. The tabs are now frames.

  restructured the classes

  **This design reached the end of his life.**

september,october,november,december 2024-...:

  **We redesigned the whole code, using the MVC-architecture.**

  all old features are now restored and improved
  
  new fullscreen gui

  recognition using webcam is perfect as long as the lighting is good




**issues:**

You shouldn't experience any issues.

**roadmap(in descending priority):**


developped by:
daanvancamp & wimnevelsteen
