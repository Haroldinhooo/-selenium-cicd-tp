import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_URL = (PROJECT_ROOT / "src" / "index.html").as_uri()

class TestCalculator:

    @pytest.fixture(scope="class")
    def driver(self):
        chrome_options = Options()
        if os.getenv('CI'):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_page_loads(self, driver):
        driver.get(INDEX_URL)

        assert "Calculatrice Simple" in driver.title
        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()

    def test_addition(self, driver):
        driver.get(INDEX_URL)
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").send_keys("5")
        Select(driver.find_element(By.ID, "operation")).select_by_value("add")
        driver.find_element(By.ID, "calculate").click()

        WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "result"), "Résultat:")
        )  
        result_text = driver.find_element(By.ID, "result").text
        assert "Résultat: 15" in result_text


    def test_division_by_zero(self, driver):
        driver.get(INDEX_URL)
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").send_keys("0")
        Select(driver.find_element(By.ID, "operation")).select_by_value("divide")
        driver.find_element(By.ID, "calculate").click()

        WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "result"), "Erreur:")
        )
        result_text = driver.find_element(By.ID, "result").text
        assert "Erreur: Division par zéro" in result_text

