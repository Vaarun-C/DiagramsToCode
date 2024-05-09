from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
import time

def init_driver() -> webdriver.Firefox:
    driver = webdriver.Firefox()
    diagrams_URL = "https://aws.amazon.com/architecture/reference-architecture-diagrams/?solutions-all.sort-by=item.additionalFields.sortDate&solutions-all.sort-order=desc&whitepapers-main.sort-by=item.additionalFields.sortDate&whitepapers-main.sort-order=desc&awsf.whitepapers-tech-category=*all&awsf.whitepapers-industries=*all"
    driver.get(diagrams_URL)
    driver.maximize_window()
    return driver

def wait_until_visible(func):
    def wrapper(driver, locator, *args, **kwargs):
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
        result = func(driver, locator, *args, **kwargs)
        return result
    return wrapper

def wait_until_clickable(func):
    def wrapper(driver, actions, locator, *args, **kwargs):
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
        result = func(driver, actions, locator, *args, **kwargs)
        return result
    return wrapper

@wait_until_visible
def get_element(driver: webdriver.Firefox, locator: str) -> WebElement:
    page_element: WebElement = driver.find_element(by=By.CSS_SELECTOR, value=locator)
    return page_element

@wait_until_clickable
def click_element(driver: webdriver.Firefox, actions: ActionChains, locator: str):
    page_element: WebElement = get_element(driver=driver, locator=locator)
    driver.execute_script("arguments[0].scrollIntoView(true);", page_element)
    actions.move_to_element(page_element)
    actions.click(page_element)
    actions.perform()

def close_browser(driver: webdriver.Firefox) -> None:
    try:
        driver.close()
    except Exception as e:
        print(f"UNABLE TO CLOSE BROWSER: {e}")
        quit()

def main() -> None:
    driver: webdriver.Firefox = init_driver()
    actions = ActionChains(driver=driver)
    max_pages = int(get_element(driver=driver, locator=".m-last-page").text)
    for _ in range(max_pages-1):
        print("CURRENT PAGE: ", get_element(driver=driver, locator="[class*='m-current-page']").text)
        click_element(driver=driver, actions=actions, locator=".m-icon-angle-right")
        time.sleep(2)
    close_browser(driver=driver)

if __name__ == "__main__":
    main()