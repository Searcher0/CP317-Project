# CP317-Project

Project Name: Grocery Guru

Requirements to Run:
Must have npm installed.
Must get chromedriver that is compatible with your chrome version. (needed for running scrappers)
   https://googlechromelabs.github.io/chrome-for-testing/

Firs
pip install -r requirements.txt

For frontend access:
1) Open terminal
2) We need to go to grocery-guru folder, to do so run the following (cd grocery-guru)
3) Next we do npm install.
4) Then npm run dev
   ![image](https://github.com/user-attachments/assets/14c2f8f7-392a-4e8b-a70a-059ed8f7e4ec)

For Backend access:
1) Open terminal
2) We need to go to Backend folder, to do so run the following (cd Backend)
3) Next run the following command (py run.py)
      Currently the scrapers are commented out from running since they take 30 min each to scrape all the content of their respective sites.
      Therefore you can uncomment them if you wish to run them. Walmart is a shorter wait if so.
4) 


To run the webscrapers for nofrills & loblaws you must download the chromedriver that corresponds to the version of chrome you are using.
Unfortunately, if you have a mac you will not be able to run the selenium library properly (based on my knowledge), therefore 2/3 scrappers will not run.
But this is no problem to see how it works, you will need to connect to the Mysql database if you want to view all the content stored there.

To run the program you need
To run backend 
Open terminal in the backend folder 
Py run.py or python3 run.py <- depends on your machine 

To run the front end 
Open terminal  in the grocery-guru folder
run
Npm install
Npm run dev
