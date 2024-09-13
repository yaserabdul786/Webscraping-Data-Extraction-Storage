from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from io import StringIO
import os
import datetime

def job():
    # Initialize the WebDriver (example with Chrome)
    driver = webdriver.Chrome()

    # Open the login page
    driver.get("https://www.myrtpos.com/newbdi/EmpRankingMark.fwx")

    # Find the username and password fields and enter your credentials
    username = driver.find_element(By.ID, "secUserID")
    password = driver.find_element(By.ID, "secPassword")

    username.send_keys("VIctoriam.texas")
    password.send_keys("Lonestar")

    # Find the login button and click it
    login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
    login_button.click()

    # Wait until the next page loads and an element on it is visible
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "table"))  # Change to a specific element on the next page
        )
        print("Login successful")
    except:
        print("Login failed")

    # Click on the "Employee Report" link
    employee_report_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='top_link' and contains(span, 'Employee Report')]"))
    )
    employee_report_link.click()

    # Click on the "Emp Ranking By Box Sales" link
    emp_ranking_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='EmpRankingMark.fwx' and contains(b, 'Emp Ranking By Box Sales')]"))
    )
    emp_ranking_link.click()

    # Wait until the target page loads and a specific element on it is visible
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "table"))  # Change to a specific element on the target page
        )
        print("Navigated to 'Emp Ranking By Box Sales' page")
    except:
        print("Failed to navigate to 'Emp Ranking By Box Sales' page")

    # Find the "All Markets" dropdown
    all_markets_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "select2-frmMarketID-container"))
    )

    # Click the dropdown
    all_markets_dropdown.click()

    # Wait for the options to be visible
    dropdown_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//li[text()='AUSTIN (4)']"))  # replace 'AUSTIN (4)' with the exact text in the dropdown
    )

    # Click the option
    dropdown_option.click()

    # Find the "Report Range" dropdown
    report_range_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'July 1, 2024 - July 4, 2024')]"))  # replace with the actual XPath of the dropdown
    )

    # Click the dropdown
    report_range_dropdown.click()

    # Wait for the options to be visible
    dropdown_option = WebDriverWait(driver, 10).until(
       EC.visibility_of_element_located((By.XPATH, "//li[@data-range-key='Today']"))  # replace 'Today' with the exact text in the dropdown
    )

    # Click the option
    dropdown_option.click()

    # Now click the "Generate" button
    generate_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='button-inner' and contains(text(), 'Generate')]"))
    )
    generate_button.click()

    # Wait until the report is generated and the table is visible
    try:
        table = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "BoxReport"))
        )
        print("Report generated successfully")

        # Extract the table data
        table_html = table.get_attribute('outerHTML')
        df = pd.read_html(StringIO(table_html))[0]

        # Filter the DataFrame for a specific employee
        employee_name = "ABDUL"  # replace with the actual employee's name
        employee_data = df[df['Username / Full Name'].str.contains(employee_name)]  # replace 'Username / Full Name' with the actual column name

        # Print the employee's data
        print(employee_data)

        # Check if the file exists
        file_exists = os.path.isfile('C:/Users/admin/Downloads/employee_data.csv')

        # Append the employee's data to a CSV file
        employee_data.to_csv('C:/Users/admin/Downloads/employee_data.csv', mode='a', index=False, header=not file_exists)

        # Append a timestamp and an empty row
        with open('C:/Users/admin/Downloads/employee_data.csv', 'a') as f:
            f.write(f"\nReport generated at {datetime.datetime.now()}\n\n")

    except Exception as e:
        print("Failed to generate the report or extract the table")
        print(e)

    # Close the WebDriver
    driver.quit()

# Run the job immediately
job()
...