import requests
import streamlit as st
import os
# FastAPI 엔드포인트 설정

PREDICT_ENDPOINT = os.getenv("PREDICT_ENDPOINT", "http://dl_service:8888/query/")

PROCESS_DOCUMENTS_ENDPOINT =  os.getenv("PROCESS_DOCUMENTS_ENDPOINT","http://dl_service:8888/process_documents/")

# Streamlit 애플리케이션 설정
st.set_page_config(page_title="RAG 기반 챗봇", page_icon="🤖", layout="wide")

# CSS to enforce text wrapping and prevent horizontal scrolling
st.markdown("""
    <style>
    /* Ensure the main container does not allow horizontal scrolling */
    .reportview-container .main .block-container {
        max-width: 800px;  /* Limit the width of content to 800px */
        overflow-x: hidden; /* Hide horizontal overflow */
        overflow-wrap: break-word; /* Break words to prevent overflow */
        word-wrap: break-word;      /* Ensure word wrap for older browsers */
        word-break: break-word;     /* Enforce word break to avoid overflow */
        white-space: normal;        /* Ensure text wraps normally */
    }
    
    /* Ensure the entire body does not allow horizontal scrolling */
    body {
        overflow-x: hidden;  /* Prevent horizontal overflow on the entire page */
    }

    /* Ensure the text area content wraps properly */
    .stText, .stMarkdown {
        word-wrap: break-word;      /* Ensure long words are wrapped */
        word-break: break-word;     /* Ensure even long strings are broken */
        white-space: normal;        /* Allow text to wrap normally */
        overflow-wrap: break-word;  /* Ensure proper wrapping of content */
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit 사이드바
with st.sidebar:
    st.title("About")
    st.markdown("""
    This is a demo UI for a RAG-based chatbot.
    You can type your query in the text box and get a response.
    """)
    # 버튼을 추가하여 문서 처리 트리거
    if st.button("Process Documents"):
        with st.spinner("Processing documents..."):
            try:
                response = requests.post(PROCESS_DOCUMENTS_ENDPOINT)
                if response.status_code == 200:
                    st.success("Documents processed and uploaded successfully!")
                else:
                    st.error(f"Error {response.status_code}: {response.json().get('detail', 'Failed to process documents.')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {str(e)}")

# Streamlit 앱 제목과 설명
st.title("🤖 RAG CHATBOT")
st.markdown("""
### Welcome to the RAG-based Chatbot!
Type your query below to get the most relevant response.
""")

# 입력 필드 및 레이아웃
query = st.text_input("Enter your query here", placeholder="e.g., How to implement RAG in Python?")

# 버튼 및 응답 처리
if st.button("Get Response"):
    if query:
        with st.spinner("Fetching the response..."):
            try:
                # 스트리밍 응답 처리
                response = requests.post(PREDICT_ENDPOINT, json={"query": query}, stream=True)
                if response.status_code == 200:
                    st.success("Here is the response:")
                    response_text = ""
                    response_area = st.empty()  # Placeholder for streaming text
                    
                    for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                        if chunk:
                            response_text += chunk
                            response_area.text(response_text)  # Display the updated response text
                else:
                    st.error(f"Error {response.status_code}: Unable to fetch response.")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {str(e)}")
    else:
        st.warning("Please enter a query to get a response.")



# 하단에 로고나 추가 설명
st.markdown("---")
st.markdown("Built with using Streamlit and FastAPI")
