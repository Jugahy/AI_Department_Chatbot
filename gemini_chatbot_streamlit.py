#!/usr/bin/env python 
# coding: utf-8

import os
import json
import streamlit as st
import google.generativeai as genai

# GenerativeAI API 키 설정
API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
genai.configure(api_key=API_KEY)

# Streamlit 앱 타이틀 설정
st.title("전주대학교 인공지능 학과 챗봇")

# JSON 파일에서 FAQ 데이터 불러오기
def load_faq_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        faq_data = json.load(file)
    return faq_data

# FAQ 데이터 불러오기
faq_data = load_faq_data('faq_data.json')

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Generative AI로 질문 응답 처리
def ask_question_with_context(question):
    context = "\n".join([f"{key}: {value}" for key, value in faq_data.items()])
    prompt = f"{context}\n\n질문: {question}"
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text

# 질문 입력 및 응답 생성
if prompt := st.chat_input("전주대학교 인공지능 학과에 대해 궁금한 것을 입력하세요:"):
    # 사용자 메시지를 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 모델 응답 생성
    answer = ask_question_with_context(prompt)
    with st.chat_message("assistant"):
        st.markdown(answer)

    # 챗봇 응답을 세션 상태에 추가
    st.session_state.messages.append({"role": "assistant", "content": answer)




