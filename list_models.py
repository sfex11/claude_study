#!/usr/bin/env python3
"""사용 가능한 Gemini 모델 목록 조회"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("❌ API 키를 찾을 수 없습니다.")
    exit(1)

print("=" * 60)
print("사용 가능한 Gemini 모델 목록 조회")
print("=" * 60)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url, timeout=30)

    if response.status_code == 200:
        result = response.json()

        if 'models' in result:
            print(f"\n총 {len(result['models'])}개의 모델 발견:\n")

            # generateContent를 지원하는 모델만 필터링
            for model in result['models']:
                name = model.get('name', '')
                display_name = model.get('displayName', '')
                supported_methods = model.get('supportedGenerationMethods', [])

                if 'generateContent' in supported_methods:
                    print(f"✅ {name}")
                    print(f"   이름: {display_name}")
                    print(f"   지원 메서드: {', '.join(supported_methods)}")
                    print()
        else:
            print("모델 목록을 찾을 수 없습니다.")
            print(f"응답: {result}")
    else:
        print(f"❌ API 요청 실패 (상태 코드: {response.status_code})")
        print(f"응답: {response.text}")

except Exception as e:
    print(f"❌ 오류 발생: {str(e)}")
