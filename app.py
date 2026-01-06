import streamlit as st
import google.generativeai as genai
import os

# 設定網頁標題
st.set_page_config(page_title="我的 AI 助手", layout="centered")

st.title("🤖 我的 Gemini AI 應用")

# 設定 API Key (優先從 Streamlit Secrets 讀取，地端則從環境變數)
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("請在 Streamlit Secrets 或環境變數中設定 GEMINI_API_KEY")
    st.stop()

# 初始化 Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash') # 你也可以換成 gemini-1.5-pro

# 初始化對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示之前的對話
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 使用者輸入
if prompt := st.chat_input("有什麼我可以幫你的嗎？"):
    # 顯示使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 呼叫 Gemini 產生回應
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # 傳送對話紀錄給 Gemini (可根據需求調整是否要帶歷史紀錄)
            response = model.generate_content(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"發生錯誤: {e}")