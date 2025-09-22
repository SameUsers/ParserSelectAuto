import asyncio
import httpx
from rabbitmq import publish


class CarList:
    def __init__(self, delay: float = 1.0):
        self.base_url = (
            "https://api2scsou.che168.com/api/v11/search?"
            "pagesize=1&sort=4&ishideback=1&srecom=2&personalizedpush=1&cid=0&"
            "iscxcshowed=-1&scene_no=12&pageid=1757089155_6308&testtype=X&"
            "test102223=X&testnewcarspecid=X&test102797=X&"
            "otherstatisticsext=%257B%2522history%2522%253A%2522%25E5%2588%2597%25E8%25A1%25A8%25E9%25A1%25B5%2522%252C%2522pvareaid%2522%253A%25220%2522%252C%2522eventid%2522%253A%2522usc_2sc_mc_mclby_cydj_click%2522%257D&"
            "filtertype=0&ssnew=1&deviceid=e9adf74b-4f21-4dd6-873f-833e1ea8edba&"
            "userid=0&s_pid=0&s_cid=0&_appid=2sc.m&v=11.41.5&_sign=a3ab783193d64735c3f758d4b12fe5bb"
        )

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/116.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://www.che168.com/",
            "Connection": "keep-alive",
        }

        self.cookies = {
            "fvlid": "175707465429550ql1RC752Bp",
            "sessionid": "e9adf74b-4f21-4dd6-873f-833e1ea8edba",
            "sessionip": "128.65.39.158",
            "area": "0",
            "showNum": "30",
            "che_sessionid": "0EF93014-C6B6-4C89-839E-F23A92ED6B79||2025-09-05+20:17:36.765||0",
            "v_no": "32",
            "visit_info_ad": "0EF93014-C6DC-4840-A43B-405800ADBA2A||-1||-1||32",
            "che_ref": "0|0|0|0|2025-09-06+00:46:56.351|2025-09-05+20:17:36.765",
            "Hm_lvt_d381ec2f88158113b9b76f14c497ed48": "1757074660,1757528179,1758104294,1758204476",
            "KEY_LOCATION_CITY_GEO_DATE": "2025918",
            "sessionuid": "e9adf74b-4f21-4dd6-873f-833e1ea8edba"
        }

        self.delay = delay  

    async def _get_json(self, client, url: str):
        try:
            r = await client.get(url)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"❌ Ошибка запроса {url}: {e}")
            return None

    async def _get_page_count(self, client) -> int:
        url = self.base_url + "&pageindex=1"
        data = await self._get_json(client, url)
        if not data or "result" not in data:
            return 0
        return data["result"].get("pagecount", 0)

    def _extract_infoid(self, data):
        infoid_list = data.get("result", {}).get("carlist", [])
        if not infoid_list:
            return None
        return str(infoid_list[0]["infoid"])

    async def get_infoid_per_page(self):
        async with httpx.AsyncClient(http2=True, headers=self.headers, cookies=self.cookies, timeout=15.0) as client:
            page_count = await self._get_page_count(client)
            print(f"🔎 Всего страниц: {page_count}")

            for page in range(1, page_count + 1):
                url = self.base_url + f"&pageindex={page}"
                data = await self._get_json(client, url)

                if data:
                    infoid = self._extract_infoid(data)
                    if infoid:
                        print(f"✅ Стр {page}: infoid={infoid}")
                        publish(infoid)
                else:
                    print(f"⚠️ Нет данных для страницы {page}")

                # задержка между запросами
                await asyncio.sleep(self.delay)


if __name__ == "__main__":
    car = CarList(delay=1.0)  
    asyncio.run(car.get_infoid_per_page())