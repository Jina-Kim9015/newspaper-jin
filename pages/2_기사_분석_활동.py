import streamlit as st
import datetime
import pandas as pd
import os
from newspaper import Article

st.set_page_config(
    page_title="생태계와 환경 기사 분석 활동",
    page_icon="📰",
    layout="centered"
)

CSV_FILE = "submitted_data.csv"

# ✅ 기사 본문 및 메타데이터 추출 함수
def extract_article_info(url):
    article = Article(url, language='ko')
    article.download()
    article.parse()
    return {
        "title": article.title,
        "authors": ", ".join(article.authors),
        "publish_date": article.publish_date.strftime("%Y-%m-%d") if article.publish_date else "",
        "text": article.text.replace("이미지 확대", "")
    }

# ✅ 관리자 뷰
st.sidebar.markdown("🧑‍🏫 **교사용 보기**")
if st.sidebar.checkbox("관리자 모드 (제출 내역 보기)"):
    st.title("📋 학생 제출 내역")
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        st.dataframe(df)
        st.download_button("📥 CSV 다운로드", df.to_csv(index=False), file_name="제출내역.csv")
    else:
        st.info("아직 제출된 데이터가 없습니다.")
    st.stop()

# ✅ 기본 정보 입력
st.title("📰 생태계와 환경 기사 분석 활동")
st.header("👤 기본 정보 입력")
student_id = st.text_input("학번을 입력하세요")
student_name = st.text_input("이름을 입력하세요")

# ✅ 기사 입력
st.header("1️⃣ 기사 링크 입력")
article_url = st.text_input("뉴스 기사 URL을 입력하세요")

article_title = ""
article_author = ""
article_source = ""
article_date = ""
article_text = ""

if article_url:
    try:
        info = extract_article_info(article_url)
        article_title = info["title"]
        article_author = info["authors"]
        article_text = info["text"]
        article_date = info["publish_date"]
        st.success("✅ 기사 정보를 자동으로 불러왔습니다.")
    except Exception:
        st.error("❌ 자동 추출 실패. 본문을 복사해서 붙여넣어 주세요.")

# ✅ 기사 본문 (자동/수동)
st.subheader("📄 기사 본문")
article_text = st.text_area("기사 본문", value=article_text, height=300)

# ✅ 메타데이터 (자동 채우기되며 수정 가능)
st.subheader("📰 기사 정보 입력")
article_title = st.text_input("기사 제목", value=article_title)
article_author = st.text_input("기자 이름", value=article_author)
article_source = st.text_input("언론사명", value=article_source)
article_date = st.text_input("발행일 (YYYY-MM-DD)", value=article_date)

# ✅ 참고문헌 APA 양식 입력
st.subheader("📚 참고문헌 (APA 양식)")
apa_citation = st.text_area("APA 양식으로 참고문헌을 작성해보세요", placeholder="예: 홍길동. (2023). 기후 변화의 영향. 한국일보.")

# ✅ 2~5번 활동
st.header("2️⃣ 이 기사를 선택한 이유")
reason = st.text_area("선택한 이유를 적어보세요", placeholder="멸종 위기종이 우리 나라에서 발견되었다는 사실에 흥미를 느낌.")

st.header("3️⃣ 기사에서 찾은 생물 다양성 관련 개념")
concepts = st.text_area("등장한 과학 개념을 적어보세요", placeholder="예: 멸종 위기 Ⅱ급은 멸종을 위한 대책을 펼치지 않으면 멸종될 가능성이 있는 생물을 의미한다.")

st.header("4️⃣ 개념의 과학적 근거")
reference = st.text_input("출처를 적어보세요 (예: 생명과학Ⅰ 교과서 190페이지, 논문, 생물다양서 사이트 등)")
if reference:
    if any(bad in reference.lower() for bad in ["블로그", "지식인", "나무위키"]):
        st.warning("⚠️ 신뢰할 수 있는 출처를 입력해야 합니다.")

st.header("5️⃣ 오개념이 있을까요?")
misconcept = st.text_area("기사에 부정확한 과학 내용이 있다면 적어보세요")

# ✅ 세션 저장
if article_title and article_text:
    st.session_state.article_data = {
        "submit_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "student_id": student_id,
        "student_name": student_name,
        "article_title": article_title,
        "article_authors": article_author,
        "article_source": article_source,
        "article_date": article_date,
        "article_text": article_text[:300],
        "apa_citation": apa_citation,
        "reason": reason,
        "concepts": concepts,
        "reference": reference,
        "misconcept": misconcept
    }

st.info("📌 다음 페이지 '문제 해결을 위한 노력'으로 이동하여 6, 7번 활동을 완료해주세요.")
