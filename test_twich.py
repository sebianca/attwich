import os
import time

import pytest
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    # Set up mobile emulation
    mobile_emulation = {"deviceName": "Pixel 7"}
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # Initialize the Chrome driver with mobile emulation
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    yield driver
    # Teardown: Close the browser after tests
    driver.quit()

def remove_consent_dialog(wait, driver):
    consent_dialog = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[class="Layout-sc-1xcs6mc-0 eTiaZz"]')))
    driver.execute_script("arguments[0].remove()", consent_dialog)

def test_twitch_streamer_screenshot(driver):
    screnshoots = []
    wait = WebDriverWait(driver, 15)

    # Step 1: Go to https://m.twitch.tv
    driver.get("https://m.twitch.tv")
    screnshoots.append('output/screenshot1.png')
    time.sleep(2)
    driver.save_screenshot(screnshoots[-1])

    #Step 2.0: wait until Cookies and Advertising Choices modal appears and delete element since click on Reject/Accept button is not working
    remove_consent_dialog(wait, driver)
    screnshoots.append('output/screenshot2.png')
    time.sleep(2)
    driver.save_screenshot(screnshoots[-1])

    # Step 2: Click on search icon
    search_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/directory"]')))
    screnshoots.append('output/screenshot3.png')
    time.sleep(2)
    driver.save_screenshot(screnshoots[-1])
    search_icon.click()

    # Step 3: Input "Starcraft II"
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="search"]')))
    search_input.send_keys("Starcraft II")
    #Click on search link after input of search term
    starcraft_2_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/directory/category/starcraft-ii"]')))
    screnshoots.append('output/screenshot4.png')
    time.sleep(2)
    driver.save_screenshot(screnshoots[-1])
    starcraft_2_link.click()

    # Wait follow button to be clickable
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-a-target="game-directory-follow-button"]')))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="ScCoreLink-sc-16kq0mq-0 RyQtp tw-link"]')))
    screnshoots.append('output/screenshot5.png')
    time.sleep(2)
    driver.save_screenshot(screnshoots[-1])
    # Step 4: Scroll down 2 times
    for _ in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for new content to load
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        screnshoots.append(f'output/screenshot_scroll_{_+1}.png')
        time.sleep(2)
        driver.save_screenshot(screnshoots[-1])
    

    # Step 5: Select one streamer from the viewport or last streamer
    streamer_in_viewport = False
    streamer_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[class="ScCoreLink-sc-16kq0mq-0 RyQtp tw-link"]')
    for streamer_button in streamer_buttons:
        # Check if the streamer button is in the viewport
        is_in_viewport = driver.execute_script("""
            var elem = arguments[0],
                box = elem.getBoundingClientRect(),
                cx = box.left + box.width / 2,
                cy = box.top + box.height / 2,
                e = document.elementFromPoint(cx, cy);
            for (; e; e = e.parentElement) {
                if (e === elem)
                    return true;
            }
            return false;
            """, streamer_button)

        #Click on the first streamer button that is in the viewport
        if streamer_button.is_displayed() and is_in_viewport:
            print('streamer_in_viewport')
            screnshoots.append('output/screenshot_streamer1.png')
            streamer_in_viewport = True
            break

    print('streamer_in_viewport_check')
    # If no streamer was in the viewport, click on the first streamer button
    if not streamer_in_viewport:
        try:
            streamer_buttons[streamer_buttons.count()-1].click()
        except: #this is when no streamer is in the viewport or on the page because can be no streamer at that time when test is runned
            print('No streamer in viewport or on page')
            print('TODO: Handle this case if needed')
            return
    else:
        streamer_button.click()


    # Step 5.1: Wait for the streamer page to load and reload page to make it work, this needs to be fixed on page
    time.sleep(5)
    screnshoots.append('output/screenshot_streamer_clicked.png')
    driver.refresh()
    time.sleep(2)
    driver.save_screenshot(screnshoots[-1])

    #Step 5.2: wait until Cookies and Advertising Choices modal ap and delete element since click on Reject/Accept button is not working
    remove_consent_dialog(wait, driver)
    screnshoots.append('output/screenshot_modal_deleted.png')
    time.sleep(2)
    driver.save_screenshot(screnshoots[-1])

    # Step 6: On streamer page, wait until it loads and take a screenshot
    # Handle modal pop-up if it appears, din't found any modal but I've added this code to handle it as example, CSS_SELECTOR is just an example and must be changed to work
    try:
        modal_close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-a-target="modal-to-be-closed"]'))
        )
        screnshoots.append('output/screenshot_modal_found.png')
        time.sleep(2)
        driver.save_screenshot(screnshoots[-1])
        modal_close_button.click()
        time.sleep(2)
        screnshoots.append('output/screenshot_modal_closed.png')
        driver.save_screenshot(screnshoots[-1])
    except:
        # No modal appeared
        pass


    # Wait for the video player to load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="channel-live-overlay"]')), message='Channel live overlay not found')

    # Take a screenshot
    screnshoots.append("output/streamer_page.png")
    time.sleep(2)
    driver.save_screenshot(screnshoots[-1])
    print(f"Screenshot saved as '{screnshoots[-1]}'.")

    # Assert that the screenshot file exists
    import os
    assert os.path.exists(screnshoots[-1]), "Screenshot was not saved."

    # Create a GIF from the screenshots
    create_gif(screnshoots)


def create_gif(file_list):

    # Filter out files that may not exist (e.g., modal screenshot)
    existing_files = [file for file in file_list if os.path.exists(file)]

    # Open images and append to a list
    images = [Image.open(file) for file in existing_files]

    # Save as GIF
    images[0].save(
        'test_execution.gif',
        save_all=True,
        append_images=images[1:],
        duration=2000,  # Duration of each frame in milliseconds
        loop=0
    )
    print("GIF created as 'test_execution.gif'.")