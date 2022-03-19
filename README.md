# HCS-SchoolFinder
이름, 생년월일로 다니는 국내에 있는 학교의 이름 찾는 유틸

## 주의
**개인정보를 부당한 수단이나 방법으로 취득하여 도용한 경우「개인정보 보호법」 제71조에 의거 처벌받을 수 있습니다.**

## 기능
+ 전국 학교 데이터 수집
+ 학교 검색

## 사용
```
import asyncio, hcs

sf = hcs.Schoolfinder('이름', '생년월일')
sf.update_db()  # 전국 학교 데이터 수집
loop = asyncio.get_event_loop()
print(loop.run_until_complete(sf.find()))  # 학교 검색
loop.close()
```
