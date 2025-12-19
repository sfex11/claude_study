#!/usr/bin/env python3
"""여러 Gemini 모델 테스트"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("❌ API 키를 찾을 수 없습니다.")
    exit(1)

# 테스트할 모델 목록
models_to_test = [
    "gemini-3.0-flash",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-pro"
]

print("=" * 70)
print("Gemini 모델 테스트")
print("=" * 70)

# 요청 데이터
data = {
    "contents": [{
        "parts": [{
            "text": "안녕하세요! 테스트 중입니다. 간단히 'OK'라고만 답변해주세요."
        }]
    }]
}

for model_name in models_to_test:
    print(f"\n📝 테스트 중: {model_name}")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    try:
        response = requests.post(url, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"   ✅ 성공! 응답: {text[:50]}")
            else:
                print(f"   ⚠️  응답 형식 오류")
        elif response.status_code == 404:
            print(f"   ❌ 모델을 찾을 수 없음 (404)")
        elif response.status_code == 403:
            print(f"   ❌ 권한 없음 (403)")
        else:
            print(f"   ❌ 실패 ({response.status_code})")

    except requests.exceptions.Timeout:
        print(f"   ⏱️  타임아웃")
    except Exception as e:
        print(f"   ❌ 오류: {str(e)[:50]}")

print("\n" + "=" * 70)
