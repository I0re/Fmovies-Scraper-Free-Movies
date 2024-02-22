import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import lackey

def scrape_fmovies(search_query):
    # Define the search URL
    search_url = f'https://ww4.fmovies.co/search/?q={search_query}'

    # Path to the CRX file
    crx_file_path = "UBlockOrigin.crx"
    crx_file_path2 = "CocoCut.crx"

    # Create Chrome WebDriver with UBlock Origin extension
    options = webdriver.ChromeOptions()
    options.add_extension(crx_file_path)
    options.add_extension(crx_file_path2)

    # Create a new instance of the Chrome driver with the specified options
    driver = webdriver.Chrome(options=options)

    # Load the search URL
    driver.get(search_url)

    # Wait for the content to be fully loaded
    time.sleep(5)

    # Get the page source after waiting
    page_source = driver.page_source

    # Close the driver
    driver.quit()

    # Parse the content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the div with id 'resdata'
    resdata_div = soup.find('div', id='resdata')
    if resdata_div:
        # Find all col elements within resdata_div
        col_elements = resdata_div.find_all('div', class_='col')
        print("Number matches found:", len(col_elements))

        # Iterate over col elements to find poster URLs and titles
        for i, col in enumerate(col_elements, 1):
            # Find the div with class card bg-transparent border-0 h-100
            card_div = col.find('div', class_='card bg-transparent border-0 h-100')
            if card_div:
                # Find the a tag containing the poster URL
                poster_url = card_div.find('a')['href']

                # Find the card-body item-title div
                item_title_div = card_div.find('div', class_='card-body item-title')
                if item_title_div:
                    # Find the h2 tag with class card-title text-light fs-6 m-0 containing the title
                    title_tag = item_title_div.find('h2', class_='card-title text-light fs-6 m-0')
                    if title_tag:
                        title = title_tag.text.strip()

                        # Print the title and URL
                        print(f"\n{i}. Title: {title}")
                        print(f"   URL: {poster_url}")

        # Ask the user to choose a number
        choice = int(input("Enter the number corresponding to the poster you want to navigate to: "))
        choice_type = int(input("Does this number correspond to a movie or series? (1 for movies, 2 for series): "))
        if choice_type == 1:
            if 1 <= choice <= len(col_elements):
                # Get the URL corresponding to the user's choice
                chosen_url = col_elements[choice - 1].find('a')['href']
                # Construct the full URL
                full_url = f"https://ww4.fmovies.co{chosen_url}"
                # Open the chosen URL in the browser
                driver = webdriver.Chrome(options=options)
                driver.get(full_url)
                # Wait for the page to fully load
                time.sleep(5)
                # Click on the play-now button and open cococut and press force download button
                try:
                    play_button = driver.find_element(By.ID, 'play-now')
                    play_button.click()
                    print("Clicked on the 'play-now' button.")

                    # Switch to the new tab
                    driver.switch_to.window(driver.window_handles[1])
                    # Wait for the page to fully load
                    time.sleep(10)

                    server_button = driver.find_element(By.ID, "srv-2")
                    server_button.click()
                    print("Clicked on the 'server' button.")
                    time.sleep(10)

                    # Get the current directory
                    current_directory = os.path.dirname(os.path.realpath(__file__))

                    # Construct the full path to the image files
                    manage_extensions_button_path = os.path.join(current_directory, "assets", "Manage_Extensions.png")
                    cococut_button_path = os.path.join(current_directory, "assets", "CocoCut_Button.png")
                    force_download_button_path = os.path.join(current_directory, "assets", "Force_Download_Button.png")

                    # Define patterns for lackey
                    pattern1 = lackey.Pattern(manage_extensions_button_path)
                    pattern2 = lackey.Pattern(cococut_button_path)
                    pattern3 = lackey.Pattern(force_download_button_path)

                    # Define main screen
                    screen = lackey.Screen()

                    # Click on the Manage extensions button
                    manage_extensions_button = screen.find(pattern1)
                    manage_extensions_button.click()
                    time.sleep(4)

                    # Find and click on the CocoCut button
                    cococut_button = screen.find(pattern2)
                    cococut_button.click()
                    time.sleep(4)

                    # Find and click on the force download button within CocoCut extension
                    force_download_button = screen.find(pattern3)
                    force_download_button.click()
                    time.sleep(4)

                    # Define the save selector to wait for
                    save_selector = (By.ID, 'dlVsaveBtn')
                    
                    try:
                        # Wait indefinitely for the element to be visible
                        element = WebDriverWait(driver, 10800).until(EC.visibility_of_element_located(save_selector))

                        # If the selector is found and visible, click on it
                        element.click()
                        print("Clicked on the element with ID 'dlVsaveBtn'.")
                        time.sleep(3)

                        # Handle the file dialog Enter key to save
                        alert = driver.switch_to.alert
                        alert.send_keys(Keys.RETURN)
                        print("Pressed Enter to save the file.")

                    except Exception as e:
                        # If an exception occurs (e.g., element not found), print the error and continue waiting
                        print("Exception occurred:", e)
                        # Sleep for a short duration before retrying
                        time.sleep(1)
                    print("Clicked on the CocoCut and force download button.")
                except Exception as e:
                    print("Failed to click either the 'play-now' or manage_extensions/CocoCut/ForceDownload button:", e)
            else:
                print("Invalid choice.")
        else:
            # Handle series selection
            print("Series selection not yet implemented. Try pressing 1. Restarting...")

    else:
        print("Could not find 'resdata' div")

# Ask the user for input
search_query = input("Enter a movie or series you want to search: ")
scrape_fmovies(search_query)
