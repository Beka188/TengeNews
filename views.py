# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from main import original_link
#
# options = Options()
# options.add_experimental_option("detach", True)
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.implicitly_wait(10)
# driver.get(original_link + '/news')
#
# # Wait for the views and comments to be loaded (adjust timeout as needed)
# def wait_until_data_views_true(driver):
#     element = driver.find_element(By.CSS_SELECTOR, '.tn-text-preloader-dark[data-views][data-type="news"]')
#     print(element.get_attribute('data-id'))
#     return element.get_attribute('data-views') != ""
#
#
# # Find the parent element that contains the views and comments
# wait = WebDriverWait(driver, 20)
# wait.until(wait_until_data_views_true)
#
# links = driver.find_elements("xpath", "//span[@class='tn-text-preloader-dark']")
#
# for link in links:
#
#     print(link.get_attribute("innerHTML"))
#
#
# driver.quit()
