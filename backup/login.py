import argparse
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

def is_logged_in(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, 'a.MyView-module__link_login___HpHMW')
        return False
    except NoSuchElementException:
        return True

def main():
    parser = argparse.ArgumentParser(description='Naver Login Automation')
    parser.add_argument('--user-data-dir', type=str, default='user.data', help='Path to user data directory for Chrome profile')
    parser.add_argument('--headless', action='store_true', help='Run Chrome in headless mode')
    parser.add_argument('--no-bot-detect', action='store_true', help='Add arguments to avoid bot detection')
    args = parser.parse_args()

    user_data_dir = os.path.abspath(args.user_data_dir)
    os.makedirs(user_data_dir, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    if args.headless:
        chrome_options.add_argument('--headless=new')
    if args.no_bot_detect:
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--lang=ko_KR')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.naver.com/')
    time.sleep(2)

    if is_logged_in(driver):
        print('Bạn đã đăng nhập Naver! Đang duy trì trạng thái đăng nhập. Nhấn Enter trong terminal để thoát.')
        input()
        driver.quit()
        return
    else:
        print('Chưa đăng nhập. Đang chuyển đến trang đăng nhập...')
        try:
            login_btn = driver.find_element(By.CSS_SELECTOR, 'a.MyView-module__link_login___HpHMW')
            ActionChains(driver).move_to_element(login_btn).click(login_btn).perform()
            print('Hãy đăng nhập thủ công trên cửa sổ trình duyệt. Khi đăng nhập xong, Naver sẽ tự chuyển về trang chủ...')
        except Exception as e:
            print('Không tìm thấy nút đăng nhập:', e)
            driver.quit()
            return

        # Chờ cho đến khi URL là trang chủ (người dùng đã đăng nhập xong)
        while True:
            time.sleep(2)
            current_url = driver.current_url
            if current_url.startswith('https://www.naver.com'):
                break
        # Khi đã về trang chủ, kiểm tra trạng thái đăng nhập thực sự
        if is_logged_in(driver):
            print('Đã đăng nhập thành công! Đang duy trì trạng thái đăng nhập. Nhấn Enter trong terminal để thoát.')
        else:
            print('Vẫn chưa đăng nhập thành công. Hãy thử lại!')
        input()
        driver.quit()

if __name__ == '__main__':
    main()
