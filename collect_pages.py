
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import ujson

chrome_options = webdriver.ChromeOptions()

ChromeDriverManager().install()
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.kca.go.kr/odr/cm/in/exmplPgItem.do"

cases = []

# 6~10페이지 수집
for page in range(6, 11):

    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(10)

    # 6페이지로 이동
    buttons = driver.find_elements(
        By.CSS_SELECTOR,
        "div.paging_pc a.btn_next"
    )
    buttons[0].click()
    time.sleep(10)

    # 7~10페이지로 이동
    if page > 6:
        page_button = driver.find_elements(
            By.CSS_SELECTOR,
            "div.paging_pc a.btn_num[onclick*=\"fn_link_page('" + str(page) + "')\"]"
        )
        page_button[0].click()
        time.sleep(10)

    titles = driver.find_elements(
        By.CSS_SELECTOR,
        "a[onclick*='fn_view_bbd']"
    )

    for i in range(len(titles)):

        titles = driver.find_elements(
            By.CSS_SELECTOR,
            "a[onclick*='fn_view_bbd']"
        )

        title = titles[i].text
        titles[i].click()
        time.sleep(10)

        soup = BeautifulSoup(
            driver.page_source, "html.parser"
        )

        question = soup.select_one("tr.qna_q span")
        answer = soup.select_one("tr.qna_a span")

        if question is not None and answer is not None:
            cases.append({
                "title": title,
                "question": question.get_text(" ", strip=True),
                "answer": answer.get_text(" ", strip=True)
            })

            # 수집할 때마다 파일 저장
            with open("consumer_cases_51_100.jsonl", "w", encoding="utf-8") as f:
                for case in cases:
                    f.write(ujson.dumps(case, ensure_ascii=False) + "\n")

            print("수집 성공:", title)

        else:
            print("수집 실패:", title)

        driver.back()
        time.sleep(10)

    print(page, "페이지 수집 완료")

print("추가 수집 성공:", len(cases))

driver.quit()

