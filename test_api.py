#!/usr/bin/env python3
"""Claude API 연결 테스트 스크립트"""

import os
from dotenv import load_dotenv
import anthropic

# 환경 변수 로드
load_dotenv()

api_key = os.getenv('ANTHROPIC_API_KEY')

print("=" * 50)
print("Claude API 연결 테스트")
print("=" * 50)

if not api_key:
    print("❌ API 키를 찾을 수 없습니다.")
    exit(1)

print(f"✅ API 키 발견: {api_key[:20]}...{api_key[-10:]}")
print("\n테스트 요청 전송 중...")

try:
    client = anthropic.Anthropic(api_key=api_key)

    # 간단한 테스트 메시지
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[
            {"role": "user", "content": "안녕하세요! 간단히 자기소개를 해주세요."}
        ]
    )

    print("\n" + "=" * 50)
    print("✅ API 연결 성공!")
    print("=" * 50)
    print(f"\n응답:\n{message.content[0].text}\n")
    print("=" * 50)
    print("🎉 Claude API가 정상적으로 작동합니다!")
    print("=" * 50)

except Exception as e:
    print(f"\n❌ 오류 발생: {str(e)}")
    exit(1)
