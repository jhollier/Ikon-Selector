################################################################################
##                                                                            ##
##                              IKON RESERVATION TOOL                         ##
##                                                                            ##
##                             Authored by J.Hollier                          ##
##                                                                            ##
## v1.1 - 1/1/2021: initial release                                           ##
##                                                                            ##
## v1.2 - 1/2/2021:                                                           ##
## - Added an implicit wait if an element is not initially found              ##
## - Commented out some forced waits in while loop                            ##
## - Combined element 'find' and 'click' into a single line                   ##
## - Reduced from 5 to 3s before refreshing                                   ##
##                                                                            ##
################################################################################

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import getpass
import time

options = Options()
options.headless = True

WELCOME_MESSAGE = """Welcome to the Ikon Reservation Assistance Tool v1.1!"""
print(WELCOME_MESSAGE)

# You can hardcore your credientials here rather than use the user prompts
# EMAIL = ""
# PASSWORD = ""
EMAIL = input('What is your ikon account email? ')
PASSWORD = getpass.getpass(prompt = 'What is your ikon account password? ')

DATE_PROMPT_TEXT ="""Input the day you are looking to find a res.
Your input MUST match this format in the below examples or the script will not work.
Ex 1: Sat Jan 02 2021
Ex 2: Thu Jan 21 2021

What day are you looking for?"""

DATE = input(DATE_PROMPT_TEXT)
# DATE = "Sat Jan 09 2021" # You can hardcode the date you're looking for here rather than use the user prompt

# options = webdriver.ChromeOptions()
# options.headless = True
USER = getpass.getuser()
PATH = "C:\\Users\\" + USER + "\\ChromeDriver\\chromedriver.exe"
driver = webdriver.Chrome(PATH,options=options)
driver.implicitly_wait(3) # Set a 3 second max wait time for web elements to load if not initially found
driver.get("https://account.ikonpass.com/en/login")

driver.find_element_by_id("email").send_keys(EMAIL)
driver.find_element_by_id("sign-in-password").send_keys(PASSWORD)
driver.find_element_by_xpath("//*[@id='scrolling-body']/section/div/div/div/div[1]/div/div/div[1]/div/form/button").click()
time.sleep(2)

driver.get("https://account.ikonpass.com/en/myaccount/add-reservations/")

found_res = False

while found_res == False:
    # time.sleep(2)
    driver.find_element_by_xpath("//*[@id='react-autowhatever-resort-picker-section-3-item-0']").click()
    # time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div/main/section[2]/div/div[2]/div[2]/div[2]/button").click()
    # time.sleep(1)
    try:
        driver.find_element_by_css_selector("div [aria-label ='" + DATE + "']:not([class*='unavailable'])").click() #https://devqa.io/selenium-css-selectors/
        found_res = True
    except:
        print("Not avaliable. Will try again in 3 seconds.")
        print('.')
        time.sleep(1)
        print('.')
        time.sleep(1)
        print('.')
        driver.refresh()

print('\n')
print('Found an open res...trying to book...')
print('\n')

driver.find_element_by_xpath("//*[@id='root']/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[2]/div/div[4]/button[1]").click() # Save button
time.sleep(1)

driver.find_element_by_xpath("//*[@id='root']/div/div/main/section[2]/div/div[2]/div[3]/div[2]/button").click() # Continue to confirmation button
time.sleep(1)

driver.find_element_by_xpath("//*[@id='root']/div/div/main/section[2]/div/div[2]/div[4]/div/div[4]/label/input").click() # I confirm checkbox
time.sleep(1)

driver.find_element_by_xpath("//*[@id='root']/div/div/main/section[2]/div/div[2]/div[4]/div/div[5]/button").click() # Confirm reservation button

print("Booked! You're ready to shred on " + DATE + "!")

# Build executable: https://datatofish.com/executable-pyinstaller/
