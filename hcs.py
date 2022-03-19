# -*- coding: utf-8 -*-
import requests, json, asyncio, aiohttp
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64encode


class Schoolfinder:
    def __init__(self, name, birthday):
        self.key = '30820122300d06092a864886f70d01010105000382010f003082010a0282010100f357429c22add0d547ee3e4e876f921a0114d1aaa2e6eeac6177a6a2e2565ce9593b78ea0ec1d8335a9f12356f08e99ea0c3455d849774d85f954ee68d63fc8d6526918210f28dc51aa333b0c4cdc6bf9b029d1c50b5aef5e626c9c8c9c16231c41eef530be91143627205bbbf99c2c261791d2df71e69fbc83cdc7e37c1b3df4ae71244a691c6d2a73eab7617c713e9c193484459f45adc6dd0cba1d54f1abef5b2c34dee43fc0c067ce1c140bc4f81b935c94b116cce404c5b438a0395906ff0133f5b1c6e3b2bb423c6c350376eb4939f44461164195acc51ef44a34d4100f6a837e3473e3ce2e16cedbe67ca48da301f64fc4240b878c9cc6b3d30c316b50203010001'
        self.sido_code = {"서울특별시": "sen", "부산광역시": "pen", "대구광역시": "dge", "인천광역시": "ice", "광주광역시": "gen", "대전광역시": "dje", "울산광역시": "use", "세종특별자치시": "sje", "경기도": "goe", "강원도": "kwe", "충청북도": "cbe", "충청남도": "cne", "전라북도": "jbe", "전라남도": "jne", "경상북도": "gbe", "경상남도": "gne", "제주특별자치도": "jje"}
        self.name = self._encryption(name)
        self.birthday = self._encryption(birthday)
        with open('./school.json', 'r') as f:
            self.school_code = json.loads(f.read())

    def _encryption(self, msg):
        key_pub = RSA.import_key(bytes.fromhex(self.key))
        cipher = Cipher_PKCS1_v1_5.new(key_pub)
        cipher_text = cipher.encrypt(msg.encode())
        return (b64encode(cipher_text)).decode('utf-8')

    async def _find_user(self, school_code, session):
        payload = {"orgCode": school_code, "name": self.name, "birthday": self.birthday, "stdntPNo": None, "loginType": "school"}
        school_info = self.school_code[school_code]
        sido = self.sido_code[school_info["sido"]]
        count = 0
        while count <= 3:
            try:
                async with session.post(f'https://{sido}hcs.eduro.go.kr/v2/findUser', json=payload) as resp:
                    if resp.status == 200:
                        return school_info['school_name']
                return
            except:
                count += 1

    def update_db(self):
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        sido_code = {"서울특별시": "1100000000", "부산광역시": "2600000000", "대구광역시": "2700000000", "인천광역시": "2800000000", "광주광역시": "2900000000", "대전광역시": "3000000000", "울산광역시": "3100000000", "세종특별자치시": "3600000000", "경기도": "4100000000", "강원도": "4200000000", "충청북도": "4300000000", "충청남도": "4400000000", "전라북도": "4500000000", "전라남도": "4600000000", "경상북도": "4700000000", "경상남도": "4800000000", "제주특별자치도": "5000000000"}
        school_code = {}
        for sido in sido_code:
            resp = requests.post("https://www.schoolinfo.go.kr/ei/ss/pneiss_a08_s0.do", verify=False, data={"SIDO_CODE": sido_code[sido]})
            for i in str(resp.text).split("\n"):
                if '<li><a href="javascript:searchSchul' in i:
                    school_code[i.split("searchSchul")[1][2:12]] = {'school_name': i.split('title="')[1].split(" 학교정보")[0], "sido": sido}
        with open('./school.json', 'w') as f:
            json.dump(school_code, f, ensure_ascii=False, indent=4)

    async def find(self):
        async with aiohttp.ClientSession() as session:
            result = await asyncio.gather(*[self._find_user(code, session) for code in self.school_code])
        while None in result:
            result.remove(None)
        return result


if __name__ == "__main__":
    sf = Schoolfinder('이름', '생년월일')
    sf.update_db()
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(sf.find()))
    loop.close()
