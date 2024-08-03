# CP317-Project

Project Name: Grocery Guru

You do not have to run the scrappers to see the working functionality, data has already been prepared in the database. You only need to follow the following Instructions to get to the working site.

Requirements to Run:
Must have npm installed. (https://nodejs.org/en)

Must get chromedriver that is compatible with your chrome version. (needed for running scrappers)
   https://googlechromelabs.github.io/chrome-for-testing/
   
Then:
pip install -r requirements.txt
For any issues later just use (npm install {whatever is missing} ex. flask
If it fails simply close vs code, & open as administrator. It is just a permissions issue.

For Backend Setup:
1) Open terminal
2) We need to go to Backend folder, to do so run the following (cd Backend)
3) Next run the following command (py run.py)
      Currently the scrapers are commented out from running since they take 30 min each to scrape all the content of their respective sites.
      Therefore you can uncomment them if you wish to run them. Walmart is a shorter wait if so.
4) Move on to the frontend setup by clicking the + button at the right side of terminal. Opening a new terminal while leaving the other active.

For Frontend Setup: (must be after backend setup)
1) Open terminal as mentioned before.
2) We need to go to grocery-guru folder, to do so run the following (cd grocery-guru)
3) Next we do (npm install).
4) Then (npm run dev)
   ![image](https://github.com/user-attachments/assets/14c2f8f7-392a-4e8b-a70a-059ed8f7e4ec)
5) Hold CTRL or option, then click the localhost link. Which leads to the website.
6) Navigate to the create list page.
7) Write any grocery Item into the search bar. Then select the closest general name that shows up.
8) Then click 'Search Cheapest Store' button. Which will the show you a pop up that will have the desired result.

When Chromedriver is downloaded adjust line 58 in loblaws scraper within the backend/scraper folder to lead to the path your chromedriver is located.
Only needed if you are trying to run that scraper.


To run the webscrapers for nofrills & loblaws you must download the chromedriver that corresponds to the version of chrome you are using.
Unfortunately, if you have a mac you will not be able to run the selenium library properly (based on my knowledge), therefore 2/3 scrappers will not run.
But this is no problem to see how it works, you will need to connect to the Mysql database if you want to view all the content stored there.
