#PyDBMS - A way to translate databases in Python

So me and my friend ARP (@adhyaatmann) had an idea back in 2025. We had studied MySQL is our school, and found the idea of databases very appealing. The only thing that approached close enough to the concept of tabular data in our syllabus was the CSV file. So, we decided to create a GUI in Python than works with CSV files in the same way as MySQL deals with its databases.

##About Our idea

So me and ARP decided that there were 2 major GUI builders in Python, namely, Tkinter and PyQt5. He decided to work with Tkinter while I chose PyQt5. We seperately built 2 programs with the same purpose, then compared the pros and cons of the projects. By the time we finished brainstorming, we both had 2 fully functional CSV handlers.

##Feature Windows

While there are a huge number of operations and commands in the program, it is easier to seperate them into different windows within the main program.

###Main Window
The starting window of the program. It can be used to open a particular CSV file, add data, remove data, or change data. The command line can also perform basic evaluation functions using the math module.
###Table Window
This is the direct successor of the Main Window. Whatever file is opened or edited using the Main Window, it is displayed on the Table Window.
###Master Editor Window
This window can do everything the Main Window does, but it also comes with extra features, like dynamic editing, comparative analysis, dynamic file saving, etc.
###New File Window
This window is basically just a basic version of Notepad, and is used to manually create and write a CSV file.
###Instructions Window
This window contains all the lists of commands of the Main Window and Master Editor Window. It acts as a reference point.

##Areas of Further Inspection 

While this program can handle most errors and exceptions through an overall try-except loop on the Main Window, some issues remain.

###The usage of EVAL
Me and ARP both strongly used the eval function throughout this whole project. It is no secret that eval can be used to run malicious code within the program. However, we have not found an equally helpful method or function yet, so it is a work in progress.
###A Console Log
ARP had this brilliant idea of putting an overall console log (just like in Python) in his program, that writes down every action committed in the program since the start. This is a very good method, and allows users to check and debug their commands easily. I have not added that, mainly because of the excess cross-window signal coding it induced. I shall think about adding it later.
###Colour Themes
ARP, being the mad coder he is, added a whole lot of VIBRANT COLOURES THEMES onto his program. Again, the cross-window coding was hard, so I avoided it. I am very less likely to see to this one.

Huge thanks to @adhyaatmann for his incredible help!