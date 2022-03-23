# HCS-SchoolFinder
이름, 생년월일로 국내에서 다니고 있는 학교의 이름을 찾는 유틸

## Disclaimer
- **개인정보를 부당한 수단이나 방법으로 취득하여 도용한 경우「개인정보 보호법」 제71조에 의거 처벌받을 수 있습니다.**
- ~~**한 아이피로 여러 번 실행시킬 시 교육부의 패치로 인해 영구 아이피 차단될 수 있습니다.**~~

## Key Features
+ 전국 학교 데이터 수집
+ 학교 검색
+ ~~프록시 지원~~

## Updating
* 2022-03-24
    * searchKey 추가
    * 아이피 차단 방지(정확하지 않음)
    * ~~프록시 추가~~


## Quick Example
```py
import asyncio, hcs

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
sf = hcs.Schoolfinder('이름', '생년월일')
sf.update_db()  # 전국 학교 데이터 수집
print(asyncio.get_event_loop().run_until_complete(sf.find())) # 학교 검색
```
