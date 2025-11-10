import time
import logging
import os

from seleniumbase import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumbase import Driver
from whatsapp_api import whatsapp_send_message
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configuration

TARGET_URL = "https://www.ticketmaster.com.br/event/venda-geral-acdc-28-02"  # Change to your target page after login
REFRESH_INTERVAL = int(os.environ.get("REFRESH_INTERVAL"))  # Seconds between refreshes
WHATSAPP_BASE_URL = os.environ.get("WHATSAPP_BASE_URL")
WHATSAPP_API_KEY = os.environ.get("WHATSAPP_API_KEY")
WHATSAPP_SESSION = os.environ.get("WHATSAPP_SESSION")
CELL_PHONE = os.environ.get("CELL_PHONE")
  
def main():

    # Initialize the SeleniumBase Driver
    hub_url = "http://localhost:4444/wd/hub"

    # Initialize the SeleniumBase Driver
    options = Options()    
    options.add_argument("start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=en")
    options.add_argument("--headless")
    #options.binary_location = '/usr/bin/firefox-nightly'
    driver = webdriver.Remote(
        command_executor=hub_url,
        options=options
    )

    search_xpath = '//*[@id="picker-bar"]/div/span'
    logging.info(f"Starting page refresh every {REFRESH_INTERVAL} seconds")
    logging.info(f"Target URL: {TARGET_URL}")
    logging.info("Press Ctrl+C to stop the script")
    
    while 1 == 1:        

        try:
            # Navigate to target page after successful login
            driver.get(TARGET_URL)       
            
            try:
                search_element = driver.wait_for_element(search_xpath, timeout=10)
                time.sleep(2)  # Wait for the element to be fully interactable
                if 'esgotado' in search_element.text.lower():
                    logging.info(f"No tickets available")
                    continue
                send_fail = whatsapp_send_message(
                    base_url=WHATSAPP_BASE_URL,
                    api_key=WHATSAPP_API_KEY,
                    session=WHATSAPP_SESSION,
                    contacts=CELL_PHONE,
                    content= f"Tickets available for: {TARGET_URL}",
                    content_type="string",
                )
                if send_fail == []:
                    logging.info("Message sent successfully to all contacts")
                    break
                else:
                    continue
                
            except Exception as e:
                logging.error(f"Error: {str(e)}")
        except KeyboardInterrupt:
            logging.info("\nScript stopped by user")
        except Exception as e:
            logging.error(f"Fatal error: {str(e)}")                
                
        # Refresh the page
        logging.info("Page refreshed successfully")

        # Wait for the next refresh
        time.sleep(REFRESH_INTERVAL)
            

if __name__ == "__main__":
    main()