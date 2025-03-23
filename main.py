import json
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(filename="errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


load_dotenv()  # Load environment variables from .env

card_email = os.getenv("EMAIL")
card_number = os.getenv("CARD_NUMBER")
card_expiry = os.getenv("CARD_EXPIRY")
card_cvc = os.getenv("CARD_CVC")
card_name = os.getenv("CARD_NAME")

url = os.getenv("URL")

def buy_ticket(email, password, event_name):
    driver = uc.Chrome()
    driver.get(url)
    
    wait = WebDriverWait(driver, 10)
    
    def sign_in(email, password):
        # sign in click
        login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Sign In')]")))
        login_button.click()

        google_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cl-button__google")))
        google_button.click()

        # Type in email
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        email_field.send_keys(email)
        email_field.send_keys(Keys.RETURN)
        print("Typed email successfully!")

        # Type in password
        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        print("Typed password successfully!")

        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]")))
        continue_button.click()

    def sign_out():
        # open account modal
        account_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cl-userButtonTrigger")))
        account_button.click()

        # sign out click
        signOut_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cl-button__signOut")))
        signOut_button.click()
        

    def navigate_to_event_detail(event_name):
        event_header =  wait.until(EC.element_to_be_clickable((By.XPATH, f"//h2[contains(., '{event_name}')]")))
        event_header.click()

    def purchase_ticket():
        try:
            # Check if 'Buy Ticket' button exists
            buy_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Buy Ticket')]")))
            buy_button.click()
            print("Clicked 'Buy Ticket'")

            # Ensure 'Purchase Your Ticket Now' button appears after clicking
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Purchase Your Ticket Now')]")))

        except TimeoutException:
            logging.error("⚠️ No 'Buy Ticket' button found. Checking if 'Purchase' button exists...")

        try:
            # Check if 'Purchase' button exists
            purchase_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Purchase Your Ticket Now')]")))
            purchase_button.click()
            print("Clicked 'Purchase Your Ticket Now'")

        except TimeoutException:
            logging.error("❌ No 'Purchase' button found. User might already have a ticket.")
            return False  # Stop further processing

        return True  # Proceed with payment if successful


    def payment_ticket():
        email_checkout = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']")))
        email_checkout.send_keys(card_email)
        cardNumber_checkout = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='cardNumber']")))
        cardNumber_checkout.send_keys(card_number)
        cardExpiry_checkout = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='cardExpiry']")))
        cardExpiry_checkout.send_keys(card_expiry)
        cardCvc_checkout = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='cardCvc']")))
        cardCvc_checkout.send_keys(card_cvc)
        billingName_checkout = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='billingName']")))
        billingName_checkout.send_keys(card_name)
        pay_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Pay')]")))
        pay_button.click()
        
    
    try:
        sign_in(email, password)
        navigate_to_event_detail(event_name)
        
        if not purchase_ticket():
            print(f"🚫 {email} already has a ticket or can't purchase one.")
            return  # Stop execution

        payment_ticket()
        sign_out()
        print(f"✅ Secure ticket for {email}")

    except Exception as e:
        logging.error(f"⚠️ Error occurred: {e}")

    finally:
        driver.quit()


with open("accounts.json", "r") as file:
    accounts = json.load(file)

account_list = list(accounts.items())
event_name = 'Aurora | This Event'

# Run multiple accounts in parallel
def main(event_name=event_name):
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(lambda acc: buy_ticket(acc[0], acc[1], event_name), account_list)
