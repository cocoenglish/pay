import textwrap
import google.generativeai as genai
import streamlit as st

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

api_key = "Google API key를 입력하세요"

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

st.title("전자기기 에너지 변환 원리 설명 애플리케이션")
st.write("전자기기의 이름을 입력하면 전기 에너지가 다른 에너지로 어떻게 변환되는지와 그 원리를 설명합니다.")

device_name = st.text_input("전자기기 이름을 입력하세요:")

if device_name:
    prompt = f"전자기기 이름: {device_name}\n전기 에너지가 다른 에너지로 어떻게 변환되며 그 원리는 무엇인가요? 상세히 설명해주세요."
    content = try_generate_content(prompt)
    
    if content:
        st.markdown(to_markdown(content))
    else:
        st.write("전자기기 정보를 가져오는 데 실패했습니다. 다시 시도해주세요.")

