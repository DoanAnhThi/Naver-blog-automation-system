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
        fill_blog_title_and_content(driver)
    except Exception as e:
        print('Không tìm thấy hoặc không thể click nút viết blog:', e)

def fill_blog_title_and_content(driver):
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

        # Nhập tiêu đề
        title_p = driver.find_element(
            By.CSS_SELECTOR,
            'div.se-title-text > p.se-text-paragraph'
        )
        driver.execute_script("arguments[0].focus();", title_p)
        ActionChains(driver).move_to_element(title_p).click(title_p).pause(0.2).click(title_p).perform()
        ActionChains(driver).move_to_element(title_p).click(title_p).send_keys(
            '🤖 인공지능(AI)의 현재와 미래: 우리는 어디로 가고 있을까?'
            ).perform()
        print('Đã nhập tiêu đề.')

        # Nhập nội dung
        content_p = driver.find_element(
            By.CSS_SELECTOR,
            'div.se-section-text > div.se-module-text > p.se-text-paragraph'
        )
        driver.execute_script("arguments[0].focus();", content_p)
        ActionChains(driver).move_to_element(content_p).click(content_p).pause(0.2).click(content_p).perform()
        ActionChains(driver).move_to_element(content_p).click(content_p).send_keys(
            '''
안녕하세요! 오늘은 요즘 가장 많이 들리는 단어 중 하나인 **AI(인공지능)**에 대해 이야기해보려 합니다. 뉴스에서, 유튜브에서, 심지어 카페 대화에서도 자주 등장하는 단어지만, 과연 우리는 인공지능에 대해 얼마나 알고 있을까요?

💡 인공지능이란 무엇인가요?
AI는 "Artificial Intelligence"의 약자로, 인간의 지능을 기계가 모방하거나 대체할 수 있도록 설계된 기술을 말합니다. 쉽게 말하면, 기계가 '생각하고 판단하고 학습하는' 능력을 가지게 만드는 기술이죠.

이러한 기술은 단순한 계산을 넘어서 자연어 처리(NLP), 이미지 인식, 자율주행, 음성 인식 등 다양한 분야에 활용되고 있습니다.

📈 지금 우리가 사용하고 있는 AI 기술들
현재 우리의 삶 곳곳에는 이미 AI가 깊숙이 들어와 있습니다.

챗봇(Chatbot): 고객센터에 문의했을 때 자동으로 응답하는 시스템

추천 알고리즘: 넷플릭스나 유튜브에서 내가 좋아할 만한 콘텐츠를 추천

스마트 스피커: “헤이 시리”, “오케이 구글”로 작동하는 음성 비서

자율주행차: 테슬라나 현대의 자율주행 기능

이미지 생성 AI: Midjourney, DALL·E, Leonardo 등을 통한 예술 창작

이러한 기술은 우리의 편의성을 높이고, 시간과 비용을 절약해주며, 때로는 창의적인 결과물까지 만들어냅니다.

🌍 AI가 바꾸고 있는 산업들
AI는 단지 기술적인 발전을 의미하는 것이 아니라, 산업 구조 자체를 변화시키고 있습니다.

1. 의료 분야
AI는 질병 진단, X-ray/CT 이미지 분석, 개인 맞춤형 치료법 개발에 활용되고 있습니다. 예측 정확도가 높아져 의료 오류를 줄이고 환자 생존율을 높이는 데 기여하고 있습니다.

2. 금융 산업
AI는 이상 거래 탐지, 신용 점수 분석, 주식 예측 모델 등에 활용됩니다. 챗GPT를 이용한 투자 조언 챗봇도 늘어나고 있습니다.

3. 교육
AI 튜터, 자동 채점 시스템, 학습 분석을 통해 맞춤형 교육이 가능해졌습니다. 특히, ChatGPT 같은 생성형 AI는 학생들의 질문에 실시간 답변을 제공하며 학습을 돕고 있습니다.

4. 마케팅 및 콘텐츠 제작
AI는 콘텐츠 작성, SNS 운영, 광고 타겟팅에 핵심적인 역할을 합니다. 특히 블로그 자동 생성, 쇼핑몰 상세페이지 작성, 인스타그램 카드뉴스 제작 등은 이제 AI의 손길이 닿지 않는 곳이 없습니다.

🧠 생성형 AI, 어디까지 왔을까?
최근 ChatGPT, Claude, Gemini, Mistral 등의 AI 모델은 단순한 검색을 넘어 창작과 사고의 영역까지 진입했습니다.

블로그 글 자동 생성

영상 대본 작성

이미지 생성

코드 개발 및 디버깅

개인 비서 역할

이제 AI는 '보조자'를 넘어 '창작자'로서의 역할까지 하고 있습니다.

🔮 AI의 미래: 가능성과 경계
AI의 미래는 무한합니다. 하지만 동시에 윤리적, 법적 문제에 대한 경계도 필요합니다.

긍정적인 미래
초개인화 서비스: 사람마다 맞춤형으로 제공되는 쇼핑, 교육, 건강관리

반복 업무 자동화로 인간의 창의성에 집중

장애인 보조 기술의 고도화로 인류 전체 삶의 질 향상

우려되는 부분
일자리 대체 문제

프라이버시 침해 및 감시 사회

**AI 편향성(Bias)**에 따른 차별적 판단

따라서, AI를 단지 ‘도구’가 아니라 인류의 동반자로 만들기 위한 고민이 절실합니다.

✅ 결론: AI와 함께 살아가기
AI는 이미 우리의 일상 깊숙이 들어와 있으며, 앞으로는 그 비중이 점점 더 커질 것입니다. 중요한 것은 AI를 어떻게 현명하게 활용하고, 동시에 책임 있게 관리할 것인지에 대한 사회적 논의입니다.

기술은 발전하되, 사람 중심의 가치를 잃지 않는 것이야말로 진정한 AI 시대의 핵심일 것입니다.

📌 질문 드려요!
당신은 AI의 미래에 대해 어떻게 생각하시나요? 댓글로 생각을 나눠주세요!

필요하시면 영어, 베트남어 버전도 제공해드릴 수 있습니다.
또한 이 글을 카드뉴스, 인스타용 요약, PDF 콘텐츠 등으로도 변환 가능합니다. 원하시는 형식이 있다면 알려주세요!
'''
            ).perform()
        print('Đã nhập nội dung.')

        driver.switch_to.default_content()
    except Exception as e:
        print('Không thể nhập tiêu đề hoặc nội dung:', e)

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
        print('Bạn đã đăng nhập Naver! Đang duy trì trạng thái đăng nhập. Chuyển đến mục blog...')
        go_to_naver_blog(driver)
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
        else:
            print('Vẫn chưa đăng nhập thành công. Hãy thử lại!')
        input('Nhấn Enter trong terminal để thoát.')
        driver.quit()

if __name__ == '__main__':
    main()
