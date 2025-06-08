from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from products.models import Deposit, Saving
from random import sample

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@api_view(['POST'])
def chatbot_response(request):
    mode = request.data.get('mode', 'recommend-form')
    # 자유 질문 모드
    if mode == 'free_text':
        user_prompt = request.data.get('free_text')
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 금융 전문가이자 친절한 도우미입니다. 사용자의 질문에 정확하고 간결하게 답변해주세요. 어투는 '요'체로 부드럽게 해주세요."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"❗ 오류 발생: {str(e)}"

        return Response({"reply": reply, "mode": mode})

    # 금융 용어 번역 모드
    elif mode == 'dict':
        text = request.data.get('text', '')
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "assistant", 
                        "content": "당신은 금융 지식을 이해하기 쉽게 풀어 쓰는 전문가이자 친절한 조언자입니다. 사용자의 질문에 정확하고 간결하게 답변해주세요. 답변 길이는 150자 내외로 제한합니다."
                    },
                    {
                        "role": "user", 
                        "content": f"기사를 읽다가 이 문장(혹은 단어)가 이해가 안됐습니다. 이 텍스트에 금융 관련 용어를 쉽게 설명해주세요. 특히 어려운 금융 용어가 있다면 그 단어의 정의는 꼭 설명하고, 문장이라면 그 문장을 쉽게 요약해주세요. 어투는 '요'체로 부드럽게 해주세요. 줄바꿈을 적절하게 사용해주세요. \n -텍스트: {text}"
                    }
                ],
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"❗ 오류 발생: {str(e)}"

        return Response({"reply": reply, "mode": mode})

    # 상품 추천 모드
    age = request.data.get('age')
    job = request.data.get('job')
    interest = request.data.get('interest')
    deposits_all = list(Deposit.objects.prefetch_related('options'))
    savings_all = list(Saving.objects.prefetch_related('options'))

    deposits = sample(deposits_all, min(len(deposits_all), 8))
    savings = sample(savings_all, min(len(savings_all), 8))

    def format_product_list(products, product_type):
        items = []
        for p in products:
            option_list = ", ".join(
                [f"{opt.save_trm}개월: {opt.intr_rate}%" for opt in p.options.all()]
            )
            items.append(
                f"{p.id}. {p.bank.name} - {p.name}\n"
                f"- 금리옵션: {option_list}\n"
                f"- 상품유형={product_type}\n"
                f"- productId={p.id}\n"
            )
        return "\n".join(items)

    product_list = format_product_list(deposits, "deposit") + "\n" + format_product_list(savings, "saving")

    system_prompt = (
        "당신은 금융 전문가입니다.\n"
        "아래 상품 목록을 참고하여 사용자의 조건에 맞는 상품을 3개 선택해 추천하고, 그 이유를 간단히 설명해 주세요.\n\n"
        " 추천 대상은 단순히 금리만이 아닌 '직업 안정성, 투자 성향, 예/적금 기간' 등을 종합적으로 고려합니다."
        "- 상품이 다양할 경우, 항상 동일한 추천이 반복되지 않도록 다양한 조건의 상품을 제시해 주세요."
        "- 설명은 간결하면서 설득력 있게, 왜 이 상품이 사용자에게 적합한지 알려주세요."
        "추천 결과는 다음 형식을 반드시 따르세요:\n\n"
        "1. [은행명 - 상품명]"
        "- 금리: [옵션들], 기간: [기간들]"
        "- 상품유형=deposit 또는 saving"
        "상품 설명 이유 (1~2줄)"

        "- productId=[상품 고유 id]\n\n"
        "상품 리스트는 실제 금융기관의 데이터이며, 이 외의 상품은 추천하지 마세요."
        # "또한 상품 productId는 출력하지 마세요"
    )

    user_prompt = f"사용자 정보: 연령대={age}, 직업={job}, 관심사={interest}\n\n[상품 목록]\n{product_list}"
    if "purpose" in request.data:
        purpose = request.data['purpose']
        period  = request.data['period']
        amount  = request.data['amount']
        user_prompt = (
            f"사용자 정보: 연령대={age}, 직업={job}, 관심사={interest}, "
            f"목적={purpose}, 기간={period}, 금액={amount}\n\n"
            f"[상품 목록]\n{product_list}"
        )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"❗ 오류 발생: {str(e)}"

    return Response({"reply": reply, "mode": mode})


