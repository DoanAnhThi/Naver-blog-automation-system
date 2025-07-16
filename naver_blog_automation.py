import argparse
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from blog_writer import generate_blog_content
import json, re

def is_logged_in(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, 'a.MyView-module__link_login___HpHMW')
        return False
    except NoSuchElementException:
        return True

def click_keep_login_checkbox(driver):
    try:
        time.sleep(1)
        keep_checkbox = driver.find_element(By.CSS_SELECTOR, 'input#nvlong')
        if not keep_checkbox.is_selected():
            keep_div = driver.find_element(By.CSS_SELECTOR, 'div#keep')
            keep_div.click()
            print('Đã tự động tích vào ô "Stay Signed in" (Duy trì đăng nhập).')
        else:
            print('Ô "Stay Signed in" đã được tích sẵn.')
    except Exception as e:
        print('Không tìm thấy hoặc không thể click ô "Stay Signed in":', e)

def go_to_naver_blog(driver):
    try:
        time.sleep(1)
        blog_btn = driver.find_element(By.CSS_SELECTOR, 'a.link_service[href="https://blog.naver.com"]')
        blog_btn.click()
        print('Đã chuyển đến mục blog của Naver.')
        time.sleep(2)
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
        click_write_blog_button(driver)
    except Exception as e:
        print('Không tìm thấy hoặc không thể click nút blog:', e)

def click_write_blog_button(driver):
    try:
        time.sleep(2)
        write_btn = driver.find_element(By.CSS_SELECTOR, 'a.item[href="https://blog.naver.com/GoBlogWrite.naver"]')
        write_btn.click()
        print('Đã click vào nút viết blog.')
        time.sleep(3)
        # fill_blog_title_and_content sẽ được gọi với keyword từ main
        # (sẽ sửa lại ở main)
    except Exception as e:
        print('Không tìm thấy hoặc không thể click nút viết blog:', e)

def fill_blog_title_and_content(driver, keyword):
    try:
        print('Chờ trang blog và iframe mainFrame xuất hiện...')
        time.sleep(5)


        # Nếu có nhiều tab, chuyển sang tab cuối cùng
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            print('Đã chuyển sang tab cuối cùng.')

        # Log tất cả các iframe hiện có
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        print(f'Có {len(iframes)} iframe trên trang:')
        for idx, iframe in enumerate(iframes):
            print(f'  [{idx}] id={iframe.get_attribute("id")}, name={iframe.get_attribute("name")}, src={iframe.get_attribute("src")}')

        # Chờ iframe xuất hiện
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'mainFrame')))
        print('Iframe mainFrame đã xuất hiện, chuẩn bị chuyển vào iframe...')
        WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'mainFrame')))
        print('Đã chuyển vào iframe mainFrame.')

        # Kiểm tra và đóng popup nếu có
        try:
            cancel_btn = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.se-popup-button.se-popup-button-cancel'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", cancel_btn)
            driver.execute_script("arguments[0].click();", cancel_btn)
            print('Đã tự động nhấn nút 취소 trên popup.')
            time.sleep(1)
        except Exception:
            print('Không có popup hoặc không cần nhấn 취소.')

        #Lấy nội dung từ OpenAI
        reply = generate_blog_content(keyword)


        # Nhập tiêu đề
        title_p = driver.find_element(
            By.CSS_SELECTOR,
            'div.se-title-text > p.se-text-paragraph'
        )
        driver.execute_script("arguments[0].focus();", title_p)
        ActionChains(driver).move_to_element(title_p).click(title_p).pause(0.2).click(title_p).perform()
        ActionChains(driver).move_to_element(title_p).click(title_p).send_keys(reply["title"]).perform()

        print('Đã nhập tiêu đề.')

        # Nhập nội dung
        content_p = driver.find_element(
            By.CSS_SELECTOR,
            'div.se-section-text > div.se-module-text > p.se-text-paragraph'
        )
        driver.execute_script("arguments[0].focus();", content_p)
        ActionChains(driver).move_to_element(content_p).click(content_p).pause(0.2).click(content_p).perform()
        ActionChains(driver).move_to_element(content_p).click(content_p).send_keys(
            # reply["intro"],reply["intro"]
            "\n\n".join([
                reply["title"],
                reply["intro"],
                reply["body"],
                reply["conclusion"]
            ])
            ).perform()

        print('Đã nhập nội dung.')

        # KHÔNG switch_to.default_content() ở đây, vì mọi thứ đều nằm trong iframe
        time.sleep(1)

        # 1. Nhấn nút phát hành đầu tiên (sau khi nhập nội dung, vẫn trong iframe)
        try:
            first_publish_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.publish_btn__m9KHH'))
            )
            first_publish_btn.click()
            print('Đã nhấn nút phát hành đầu tiên (trong iframe).')
        except Exception as e:
            print('Không tìm thấy hoặc không thể click nút phát hành đầu tiên trong iframe:', e)
            return

        # 2. Đợi popup hiện ra, nhập tag (vẫn trong iframe)
        try:
            tag_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#tag-input, input.tag_input__rvUB5'))
            )
            tag_input.clear()
            tag_input.send_keys(reply["tags"])
            tag_input.send_keys(Keys.ENTER)
            print('Đã nhập tag.')
        except Exception as e:
            print('Không tìm thấy hoặc không thể nhập tag:', e)
            return

        # 3. Trước khi nhấn nút "발행" trên popup để đăng bài (vẫn trong iframe), chuyển sang chế độ hẹn giờ và chọn thời gian đăng sau 30 phút
        try:
            # Nhấn vào nút 예약 (hẹn giờ)
            schedule_radio = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="radio_time2"].radio_label__mB6ia'))
            )
            schedule_radio.click()
            print('Đã chọn chế độ 예약 (hẹn giờ).')
            time.sleep(1)

            # Tính toán thời gian đăng sau 30 phút
            from datetime import datetime, timedelta
            now = datetime.now()
            future = now + timedelta(minutes=30)
            hour_str = future.strftime('%H')
            minute = future.minute
            # Làm tròn xuống theo các option 00, 10, 20, 30, 40, 50
            minute_rounded = (minute // 10) * 10
            minute_str = f'{minute_rounded:02d}'

            # Chọn giờ
            hour_select = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'select.hour_option__J_heO'))
            )
            hour_select.click()
            from selenium.webdriver.support.ui import Select
            Select(hour_select).select_by_value(hour_str)
            print(f'Đã chọn giờ: {hour_str}')

            # Chọn phút
            minute_select = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'select.minute_option__Vb3xB'))
            )
            minute_select.click()
            Select(minute_select).select_by_value(minute_str)
            print(f'Đã chọn phút: {minute_str}')
        except Exception as e:
            print('Không thể hẹn giờ đăng bài:', e)

        # 4. Nhấn nút "발행" trên popup để đăng bài (vẫn trong iframe) - ĐANG TẮT CODE NÀY THEO YÊU CẦU
        try:
            final_publish_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.confirm_btn__WEaBq[data-testid="seOnePublishBtn"], button.confirm_btn__WEaBq'))
            )
            final_publish_btn.click()
            print('Đã nhấn nút phát hành (đăng bài) thành công!')
        except Exception as e:
            print('Không tìm thấy hoặc không thể click nút phát hành:', e)
            return

    except Exception as e:
        print('Không thể nhập tiêu đề hoặc nội dung:', e)

def main(keyword):
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
        print('Bạn đã đăng nhập Naver! Đang duy trì trạng thái đăng nhập. Chuyển đến mục blog...')
        go_to_naver_blog(driver)
        fill_blog_title_and_content(driver, keyword)
        input('Nhấn Enter trong terminal để thoát.')
        driver.quit()
        return
    else:
        print('Chưa đăng nhập. Đang chuyển đến trang đăng nhập...')
        try:
            login_btn = driver.find_element(By.CSS_SELECTOR, 'a.MyView-module__link_login___HpHMW')
            ActionChains(driver).move_to_element(login_btn).click(login_btn).perform()
            print('Hãy đăng nhập thủ công trên cửa sổ trình duyệt. Khi đăng nhập xong, Naver sẽ tự chuyển về trang chủ...')
            time.sleep(2)
            click_keep_login_checkbox(driver)
        except Exception as e:
            print('Không tìm thấy nút đăng nhập:', e)
            driver.quit()
            return

        while True:
            time.sleep(2)
            current_url = driver.current_url
            if current_url.startswith('https://www.naver.com'):
                break
        if is_logged_in(driver):
            print('Đã đăng nhập thành công! Đang chuyển đến mục blog...')
            go_to_naver_blog(driver)
            fill_blog_title_and_content(driver, keyword)
        else:
            print('Vẫn chưa đăng nhập thành công. Hãy thử lại!')
        input('Nhấn Enter trong terminal để thoát.')
        driver.quit()

if __name__ == '__main__':
    keyword = input('Nhập từ khóa cho bài viết: ')
    main(keyword)
