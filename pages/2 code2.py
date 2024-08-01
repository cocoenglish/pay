import textwrap
import google.generativeai as genai
import streamlit as st
import pathlib
import toml

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
api_key = secrets.get("api_key")

# API 키를 설정
genai.configure(api_key=api_key)

# 설정된 모델 변경
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config={
                                  "temperature": 0.9,
                                  "top_p": 1,
                                  "top_k": 1,
                                  "max_output_tokens": 2048,
                              },
                              safety_settings=[
                                  {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                              ])

# 콘텐츠 생성 시도
def try_generate_content(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"API 호출 실패: {e}")
        return None

st.title("원소 정보 제공 애플리케이션")
st.write("원소 이름을 입력하면 해당 원소의 특징과 우리 생활에서 많이 사용하는 물질을 알려드립니다.")

element_name = st.text_input("원소 이름을 입력하세요:")

if element_name:
    prompt = f"원소 이름: {element_name}\n특징과 우리 생활에서 많이 사용하는 물질에 대해 설명해주세요."
    content = try_generate_content(prompt)
    
    if content:
        st.markdown(to_markdown(content))
    else:
        st.write("원소 정보를 가져오는 데 실패했습니다. 다시 시도해주세요.")
