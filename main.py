import logging
import logging.handlers
import os
from datetime import datetime

import pandas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

BASE_FILE_NAME = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
FILE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
LOG_FOLDER = os.path.join(FILE_DIRECTORY,'logs')
LOGNAME = os.path.join(LOG_FOLDER,f"{BASE_FILE_NAME}{datetime.now().strftime('%d_%b_%H_%M_%S')}.log")
USERNAME='kkausthubcool123@gmail.com'
PASSWORD='kkausthubcool123'
print(f"Log file location : {LOGNAME}")

def set_logger():
    os.makedirs(LOG_FOLDER, exist_ok=True)
    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(filename=LOGNAME)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(funcName)s][%(levelname)s] %(message)s',datefmt='%d/%b/%y %I:%M:%S %p %Z')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


class UdemyScraper:
    def __init__(self):
        self.UDEMY_PAGE_LIST = [r"C:\Users\Kausthub\Downloads\page.html",r"C:\Users\Kausthub\Downloads\page2.html",r"C:\Users\Kausthub\Downloads\page3.html",r"C:\Users\Kausthub\Downloads\page4.html",r"C:\Users\Kausthub\Downloads\page5.html",r"C:\Users\Kausthub\Downloads\page6.html"]
        self.excel_sheet = pandas.DataFrame(columns=['Question', 'Answer', 'Explanation'])
        self.logger = set_logger()
        self.SetupChromeDriver()
        self.openEpicGamesLogin()



    def SetupChromeDriver(self):
        self.options = Options()
        self.options.add_argument('--no-sandbox')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        self.options.add_argument("disable-infobars")
        self.options.add_argument("headless")
        self.options.add_experimental_option('useAutomationExtension', False)
        self.chrome_driver_path = r"chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=self.options)
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )


    def openEpicGamesLogin(self):
        for udemy_page in self.UDEMY_PAGE_LIST:
            self.driver.get(udemy_page)
            no_of_ques = self.driver.find_elements(By.CSS_SELECTOR,value="form[class='mc-quiz-question--container--3GZ4h']")
            for ques in no_of_ques:
                ques_no = ques.find_element(By.TAG_NAME,'span')
                # print(ques_no.text,end='\t')
                question_text = ques.find_element(By.ID,'question-prompt')
                # print(question_text.text)
                options = ques.find_elements(By.CSS_SELECTOR,value="div[class='udlite-heading-md']")
                option_list = []
                correct_answers = []
                start_option = 'A'
                for option in options:
                    if '(Correct)' in option.text:
                        correct_answers.append(start_option)
                    option_list.append(start_option + '.' +option.text.replace('(Correct)','').replace('(Incorrect)',''))
                    start_option = chr(ord(start_option)+1)
                # print('\n'.join(option_list))
                # print('Correct Answers')
                # print('\n'.join(correct_answers))
                try:
                    explanation = ques.find_element(By.ID,value='question-explanation').text
                except:
                    explanation = ""
                final_question_text = question_text.text + "\n" + '\n'.join(option_list)
                final_correct_answers = ''.join(correct_answers)
                row = [final_question_text,final_correct_answers,explanation]
                self.excel_sheet.loc[len(self.excel_sheet.index)] = row




usc = UdemyScraper()
usc.excel_sheet.to_excel('question.xlsx')

