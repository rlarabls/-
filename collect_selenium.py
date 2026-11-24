
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

chrome_options = webdriver.ChromeOptions()

ChromeDriverManager().install()
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.kca.go.kr/odr/cm/in/exmplPgItem.do"

# 1. 한국소비자원 홈페이지 접속
driver.get(url)
driver.implicitly_wait(10)
time.sleep(3)

# 2. 피해구제사례 제목 찾기
titles = driver.find_elements(
    By.CSS_SELECTOR, "a[onclick*='fn_view_bbd']"
)

print("수집한 제목 개수:", len(titles))


# 3. 피해구제사례 10개 수집
cases = []

for i in range(10):
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(10)

    titles = driver.find_elements(
        By.CSS_SELECTOR, "a[onclick*='fn_view_bbd']"
    )

    title = titles[i].text
    titles[i].click()
    time.sleep(10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    content = soup.get_text(separator="\n", strip=True)

    # 질문과 답변 추출
    question = soup.select_one("tr.qna_q")
    answer = soup.select_one("tr.qna_a")

    if question is not None and answer is not None:
        cases.append({
            "title": title,
            "question": question.get_text(" ", strip=True),
            "answer": answer.get_text(" ", strip=True)
        })
        print(i + 1, "번 사례 수집 성공:", title)
    else:
        print(i + 1, "번 사례 수집 실패:", title)

# 수집 결과 확인
print("총 수집 성공:", len(cases))

for case in cases:
    print("====================")
    print("제목:", case["title"])
    print("질문:", case["question"])
    print("답변:", case["answer"])

driver.quit()

import ujson

with open("consumer_cases.jsonl", "w", encoding="utf-8") as f:
    for case in cases:
        f.write(ujson.dumps(case, ensure_ascii=False) + "\n")

print("JSONL 파일 저장 완료:", len(cases), "개")
