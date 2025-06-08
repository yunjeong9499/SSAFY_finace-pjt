import requests
import os 

from django.core.management.base import BaseCommand
from products.models import Saving, SavingOption, Bank
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
BANK_GROUPS = ["020000", "030300", "050000", "060000", "070000"]

class Command(BaseCommand):
    help = "Fetch ALL saving products from FSS for all bank groups"

    def handle(self, *args, **kwargs):
        total_saved = 0

        for group_code in BANK_GROUPS:
            page = 1
            self.stdout.write(self.style.NOTICE(f"📂 {group_code} 은행권 적금 처리 시작"))

            while True:
                response = requests.get(BASE_URL, params={
                    "auth": API_KEY,
                    "topFinGrpNo": group_code,
                    "pageNo": page
                })

                print(f"\n📡 [{group_code}] 페이지 {page} 요청 URL: {response.url}")
                print(f"✅ 응답 상태 코드: {response.status_code}")

                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f"❌ API 호출 실패 (페이지 {page})"))
                    break

                data = response.json()
                result = data.get("result")

                if not result:
                    self.stdout.write(self.style.ERROR("❌ result가 응답에 없음 (인증키 오류 가능)"))
                    break

                base_list = result.get("baseList", [])
                option_list = result.get("optionList", [])

                if not base_list:
                    self.stdout.write(self.style.WARNING(f"⚠️ 페이지 {page}: baseList가 비어 있음"))
                    break

                for item in base_list:
                    bank_name = item['kor_co_nm']
                    bank, _ = Bank.objects.get_or_create(name=bank_name)

                    saving, created = Saving.objects.update_or_create(
                        saving_code=item['fin_prdt_cd'],
                        defaults={
                            "bank": bank,
                            "name": item['fin_prdt_nm'],
                            "join_way": item.get('join_way'),
                            "mtrt_int": item.get('mtrt_int'),
                            "spcl_cnd": item.get('spcl_cnd'),
                            "join_deny": int(item['join_deny']),
                            "join_member": item.get('join_member'),
                            "etc_note": item.get('etc_note'),
                            "max_limit": item.get('max_limit') or None,
                            "dcls_month": item['dcls_month'],
                        }
                    )
                    total_saved += 1

                for opt in option_list:
                    print("📌 적금 금리 저장:", opt.get('fin_prdt_cd'), opt.get('save_trm'),
                          opt.get('intr_rate'), opt.get('intr_rate2'))

                    saving = Saving.objects.filter(saving_code=opt['fin_prdt_cd']).first()
                    if saving:
                        SavingOption.objects.update_or_create(
                            saving=saving,
                            save_trm=opt['save_trm'],
                            defaults={
                                "intr_rate": opt.get('intr_rate') or 0.0,
                                "intr_rate2": opt.get('intr_rate2') or 0.0,
                                "intr_rate_type_nm": opt.get('intr_rate_type_nm'),
                            }
                        )

                self.stdout.write(self.style.SUCCESS(f"✅ [{group_code}] 페이지 {page} 완료"))
                page += 1

        self.stdout.write(self.style.SUCCESS(f"🎉 전체 은행권 적금 상품 {total_saved}개 저장 완료"))
