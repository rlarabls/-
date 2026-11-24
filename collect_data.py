
import requests
from bs4 import BeautifulSoup

# 1. 한국소비자원 웹페이지 접속
url = "https://www.kca.go.kr/odr/cm/in/exmplPgItem.do"

res = requests.get(url)
html = res.text

# 2. HTML 분석
soup = BeautifulSoup(html, "html.parser")

# 3. 피해구제사례 제목 추출
titles = soup.select("a[onclick*='fn_view_bbd']")

# 4. 수집한 제목 출력
print("수집한 제목 개수:", len(titles))

for title in titles:
    print(title.get_text(strip=True))


