from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


def read_credentials_from_file(filename="accounts.txt"):
    credentials = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and ':' in line:
                    credentials.append(line)
        print(f"Successfully loaded {len(credentials)} accounts from file")
        return credentials
    except FileNotFoundError:
        print(f"File {filename} not found in project root!")
        return []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []


# Load credentials from file
credentials = read_credentials_from_file()

if not credentials:
    print("No data to check. Exiting.")
    exit()

chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Initialize driver with options
driver = webdriver.Chrome(options=chrome_options)


def wait_and_click(selector, timeout=12):
    """Improved wait and click function"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        driver.execute_script("arguments[0].click();", element)
        return element
    except Exception as e:
        print(f"Error clicking element {selector}: {str(e)}")
        raise


def check_account_status():
    """Check account status after login"""
    try:
        WebDriverWait(driver, 12).until(
            lambda d: any([
                "phone-link" in d.current_url,
                "account/profile" in d.current_url,
                "unblock/support" in d.current_url
            ])
        )

        if "unblock/support" in driver.current_url:
            return "DEAD"
        elif "account/profile" in driver.current_url:
            return "LIVE"
        elif "phone-link" in driver.current_url:
            return "PHONE_NEEDED"

    except Exception as e:
        print(f"Error checking status: {str(e)}")
        return "UNKNOWN"


for cred in credentials:
    try:
        login, password = cred.split(":", 1)  # Split only by first colon
        print(f"\nProcessing account: {login}")

        # 1. Go to login page
        driver.get("https://id.rambler.ru/login-20/login")

        # 2. Enter credentials
        wait_and_click("#login").send_keys(login)
        driver.find_element(By.ID, "password").send_keys(password)
        wait_and_click("button[type='submit']")

        # 3. Check account status
        status = check_account_status()

        if status == "DEAD":
            print(f"✖ {login} - blocked (DEAD)")
            continue

        elif status == "PHONE_NEEDED":
            print(f"⚠ {login} - requires phone verification")
            wait_and_click("button.styles_confirmLater___bpNl")
            WebDriverWait(driver, 12).until(
                EC.url_contains("account/profile"))
            print(f"✔ {login} - login successful (LIVE)")

        elif status == "LIVE":
            print(f"✔ {login} - login successful (LIVE)")

        # 4. Logout
        try:
            time.sleep(8)
            driver.get("https://id.rambler.ru/logout")
            print("↩ Logout successful")

        except Exception as logout_error:
            print(f"Logout error: {str(logout_error)}")
            driver.get("https://id.rambler.ru/logout")

    except Exception as main_error:
        print(f"⚠ Critical error: {str(main_error)}")
        driver.save_screenshot(f"error_{login.split('@')[0]}.png")

    # Pause between requests
    time.sleep(3)

driver.quit()
print("\n" + "=" * 50)
print("Check completed. Results:")
print(f"Total accounts: {len(credentials)}")
print("=" * 50)