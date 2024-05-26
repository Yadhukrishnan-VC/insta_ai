from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pdb
import time



class InstaAutomation:
    def __init__(self, base_url):
        self.base_url = base_url
        self.user_input()
        self.choose_options()
        self.user_option()
        self.start()
        self.login()
        self.start_task()
        
    def user_input(self):
        username_inp = input("Enter Username: ")
        password_inp = input("Enter Password: ")
        tfa = input("Is Two Factor Authentication enabled: (yes/no) ")

        if tfa == "yes":
            print("Please enter the OTP in the browser...")
        elif tfa != "no":
            print("Please enter 'yes'/'no' ")
            exit()
        self.username_inp = username_inp 
        self.password_inp = password_inp 
        self.tfa = tfa
            
    def choose_options(self):
        print("#######~~~Options~~~#########")  
        print("1) Unfollow all users whoes doesn't follow back")  
        print("2) Unfollow the users whoes doesn't follow back except celebrities")  
        print("3) Follow back the users whoes follow you")  
        print("4) Unfollow users in given list")  
        print("5) Follow users in given list")

        option = int(input("Please select an option: [1-5] "))

        if option not in range(1,6):
            print("Please select an option")
            exit()
        self.option = option
    
    def user_option(self):
        # TO-DO : code for all options
        if self.option == 4:
            unfollow_list = input("Please provide the users list for unfollow (comma-separated): ")
            self.unfollow_list = list(map(str.strip, unfollow_list.split(',')))
        elif self.option == 5:
            follow_list = input("Please provide the users list for unfollow (comma-separated): ")
            self.follow_list = list(map(str.strip, follow_list.split(',')))
        
    def start(self):
        self.driver = webdriver.Chrome()
        self.driver.get(BASE_URL)

        if self.tfa == "yes":
            time.sleep(50)
        print("Starting........")
        
    def login(self):
        username = self.driver.find_element(By.NAME, 'username')
        password = self.driver.find_element(By.NAME, 'password')

        username.send_keys(self.username_inp)
        password.send_keys(self.password_inp)

        login_button = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")

        for login in login_button:
            if 'Log in' in login.text :
                login.click()
                break
        time.sleep(5)
        
    def start_task(self):
        if self.option == 4 and self.unfollow_list:
            self.unfollow_users_from_list(self.unfollow_list)
        elif self.option == 5 and self.follow_list:
            self.follow_users_from_list(self.follow_list)
        
    def unfollow_users_from_list(self,unfollow_list):
        except_list = []
        for usr in unfollow_list:
            print("user profile url ::: ",f'{BASE_URL}{usr}')
            self.driver.get(f'{BASE_URL}{usr}')

            time.sleep(2)
            WebDriverWait(self.driver, 10).until(            
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            
            buttons = self.driver.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                try:
                    if 'Following' in button.text:
                        button.click()
                        unfollow_span = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//span[text()='Unfollow']"))
                        )
                        unfollow_span.click()
                        print(f"Clicked 'Unfollow' button for user: {usr}")

                except Exception as e:
                    print("Eror:::",e)
                    except_list.append(usr)
                    pass
        print("Some Exceptions occured users >>>",except_list)
        
    def follow_users_from_list(self,follow_list):
        except_list = []
        for usr in follow_list:
            print("user profile url ::: ",f'{BASE_URL}{usr}')
            self.driver.get(f'{BASE_URL}{usr}')

            time.sleep(2)
            WebDriverWait(self.driver, 10).until(            
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            
            buttons = self.driver.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                try:                        
                    if 'Follow' in button.text:
                        button.click()
                        print(f"Clicked 'follow' button for user: {usr}")
                except Exception as e:
                    print("Eror:::",e)
                    except_list.append(usr)
                    pass
        print("Some Exceptions occured users >>>",except_list)
        
    def close(self):
        self.driver.quit()
        
    #Profile 
    # driver.refresh()
    # driver.get(f'{BASE_URL}{username_inp}/following')
    # driver.refresh()

    # TO-DO : taking the following list and followers list from the profile or import data and extract

    # time.sleep(1)

    # def scroll_down(driver):
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # # Get initial page height
    # last_height = driver.execute_script("return document.body.scrollHeight")

    # while True:
    #     # Scroll down to the bottom
    #     scroll_down(driver)
        
    #     # Wait for new content to load
    #     time.sleep(2)
        
    #     # Calculate new page height and compare with last height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
        
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

    # # Extract all href attributes from links
    # links = driver.find_elements(By.TAG_NAME, 'a')
    # hrefs = [link.get_attribute('href') for link in links]
    # pdb.set_trace()
    # button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'following')]"))
    # )
    # button.click()
    # time.sleep(2)

if __name__ == "__main__":
    BASE_URL = 'https://www.instagram.com/'
    automation = InstaAutomation(BASE_URL)
    automation.close()
