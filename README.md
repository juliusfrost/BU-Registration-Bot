# BU Class Registration Bot

With BU Ninja becoming more and more widespread, it is becoming harder to get the class you want. With this bot, however, you can beat the competition for free! (at the moment)  
Leave this bot running on a machine and it will constantly check availability of a course and automatically register for it.

## Prerequisites
Minimal knowledge of Python  
A machine available to run the program 24/7

## Installation
Clone the repository to Desktop or Download ZIP and extract  
Make sure you have Python installed with Anaconda

Using Anaconda, run this command
`pip install selenium`  

Google search and download `chrome webdriver`, extract to somewhere safe, and add the file path to PATH (in envirionment variables for windows users).  
Restart your computer for it to register.  
Open the reg.py file with a text editor, and edit the credentials method with your BU login and courses list with the info of the courses you desire.  
Finally, run the file and wait.

### Optional
If you want you can change which browser to open with Selenium. Goto http://selenium-python.readthedocs.io/api.html  
Then replace this on line 91: `driver = webdriver.Chrome()` to whatever browser you desire. (Note that you might have to install a different web driver for that)    
For AWS, find out how to install PhantomJS as it doesn't require any GUI. For PhantomJS it would look like `driver = webdriver.PhantomJS()`.

## How it works
Using the Selenium API, the script opens a browser and automatically logs you into the BU Student link. After that it grabs the cookies and closes the browser. Then it sends queries to the course browsing page and when your class is open, it grabs the course selection ID and registers by making a request with that information.
