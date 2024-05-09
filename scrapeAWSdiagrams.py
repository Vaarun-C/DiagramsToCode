from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement

def init_driver() -> webdriver.Firefox:
    driver = webdriver.Firefox()

    diagrams_URL = "https://aws.amazon.com/architecture/reference-architecture-diagrams/?solutions-all.sort-by=item.additionalFields.sortDate&solutions-all.sort-order=desc&whitepapers-main.sort-by=item.additionalFields.sortDate&whitepapers-main.sort-order=desc&awsf.whitepapers-tech-category=*all&awsf.whitepapers-industries=*all"
    driver.get(diagrams_URL)

    driver.maximize_window()
    return driver

def wait_until_visible(func):
    def wrapper(driver, locator, *args, **kwargs):
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
        result = func(driver, locator, *args, **kwargs)
        return result
    return wrapper

@wait_until_visible
def get_max_pages(driver: webdriver.Firefox, locator: str) -> int:
    last_page_element: WebElement = driver.find_element(by=By.CSS_SELECTOR, value=locator)
    last_page_element_text = last_page_element.text
    return int(last_page_element_text)

def close_browser(driver: webdriver.Firefox) -> None:
    try:
        driver.close()
    except Exception as e:
        print(f"UNABLE TO CLOSE BROWSER: {e}")
        quit()

def main() -> None:
    driver: webdriver.Firefox = init_driver()
    actions = ActionChains(driver=driver)
    print("MAX PAGES: ", get_max_pages(driver=driver, locator=".m-last-page"))
    close_browser(driver=driver)

if __name__ == "__main__":
    main()