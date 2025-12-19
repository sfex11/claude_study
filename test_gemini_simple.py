#!/usr/bin/env python3
"""Gemini 3.0 Flash 모델 테스트 (REST API 사용)"""

import os
import requests
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')

print("=" * 60)
print("Gemini 3.0 Flash 모델 테스트")
print("=" * 60)

if not api_key:
    print("❌ API 키를 찾을 수 없습니다.")
    exit(1)

print(f"✅ API 키 발견: {api_key[:20]}...{api_key[-10:]}")

# Gemini API endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.0-flash:generateContent?key={api_key}"

# 요청 데이터
data = {
    "contents": [{
        "parts": [{
            "text": "안녕하세요! Gemini 3.0 Flash 모델이 정상적으로 작동하는지 테스트 중입니다. 간단히 자기소개를 해주세요."
        }]
    }]
}

print("\n테스트 요청 전송 중...")
print(f"모델: gemini-3.0-flash")

try:
    response = requests.post(url, json=data, timeout=30)

    if response.status_code == 200:
        result = response.json()

        if 'candidates' in result and len(result['candidates']) > 0:
            text = result['candidates'][0]['content']['parts'][0]['text']

            print("\n" + "=" * 60)
            print("✅ API 연결 성공!")
            print("=" * 60)
            print(f"\n응답:\n{text}\n")
            print("=" * 60)
            print("🎉 Gemini 3.0 Flash 모델이 정상적으로 작동합니다!")
            print("=" * 60)
        else:
            print("\n❌ 응답 형식이 예상과 다릅니다.")
            print(f"응답: {result}")
    else:
        print(f"\n❌ API 요청 실패 (상태 코드: {response.status_code})")
        print(f"응답: {response.text}")

        if response.status_code == 404:
            print("\n⚠️  gemini-3.0-flash 모델을 찾을 수 없습니다.")
            print("사용 가능한 모델을 확인해보세요.")

except requests.exceptions.Timeout:
    print("\n❌ 요청 시간 초과")
except Exception as e:
    print(f"\n❌ 오류 발생: {str(e)}")
    exit(1)
