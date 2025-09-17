import requests
import redis
from rabbitmq import publish

class CarList:
    def __init__(self):
        self.redis = redis.Redis(host = 'redis', port = 6379, db=0, password='mypassword')

        self.headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                        "Chrome/116.0.0.0 Safari/537.36",
                            "Accept": "application/json, text/plain, */*",
                            "Accept-Language": "zh-CN,zh;q=0.9",
                            "Referer": "https://www.che168.com/",
                            "Connection": "keep-alive"
                            }
        
        self.cookies = {
                        "ahpvno": "41",
                        "fvlid": "175707465429550ql1RC752Bp",
                        "sessionid": "e9adf74b-4f21-4dd6-873f-833e1ea8edba",
                        "sessionip": "128.65.39.158",
                        "area": "0",
                        "sessionvisit": "18819c94-2fc6-4323-b5d9-46422cdfbbe2",
                        "sessionvisitInfo": "e9adf74b-4f21-4dd6-873f-833e1ea8edba||0",
                        "ahuuid": "AD7F63AC-BA6E-46F1-9381-79992D314371",
                        "showNum": "7",
                        "che_sessionid": "0EF93014-C6B6-4C89-839E-F23A92ED6B79||2025-09-05+20:17:36.765||0",
                        "v_no": "25",
                        "visit_info_ad": "0EF93014-C6B6-4C89-839E-F23A92ED6B79||73015ECA-409A-48E8-924E-AC79BE6DC22B||-1||-1||25",
                        "che_ref": "0|0|0|0|2025-09-05+22:13:00.939|2025-09-05+20:17:36.765",
                        "che_sessionvid": "73015ECA-409A-48E8-924E-AC79BE6DC22B",
                        "Hm_lvt_d381ec2f88158113b9b76f14c497ed48": "1757074660",
                        "Hm_lpvt_d381ec2f88158113b9b76f14c497ed48": "1757080317",
                        "HMACCOUNT": "97F91CE39247D76B",
                        "userarea": "0",
                        "listuserarea": "0",
                        "_ac": "Pwe5i03GrrAPwGcqd_9ciVF6UgMvD6zpLpNgSe9hlU7sBxlq2KwS",
                        "KEY_LOCATION_CITY_GEO_DATE": "202595",
                        "sessionuid": "e9adf74b-4f21-4dd6-873f-833e1ea8edba"
                        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)

        
    def _get_json(self, url):
        response = self.session.get(url)
        self.result = response.json()
        return self.result
    

    def _get_page_count(self):
        start_page = self._get_json("https://api2scsou.che168.com/api/v11/search?pageindex=1&pagesize=1&sort=4&ishideback=1&srecom=2&personalizedpush=1&cid=0&iscxcshowed=-1&scene_no=12&pageid=1757089155_6308&testtype=X&test102223=X&testnewcarspecid=X&test102797=X&otherstatisticsext=%257B%2522history%2522%253A%2522%25E5%2588%2597%25E8%25A1%25A8%25E9%25A1%25B5%2522%252C%2522pvareaid%2522%253A%25220%2522%252C%2522eventid%2522%253A%2522usc_2sc_mc_mclby_cydj_click%2522%257D&filtertype=0&ssnew=1&deviceid=e9adf74b-4f21-4dd6-873f-833e1ea8edba&userid=0&s_pid=0&s_cid=0&_appid=2sc.m&v=11.41.5&_sign=a3ab783193d64735c3f758d4b12fe5bb")
        page_count = start_page['result']['pagecount']
        return page_count
    

    def _get_infoid_from_page(self, json):
        infoid_list = json['result'].get('carlist', [])
        if not infoid_list:
            return None
        return str(infoid_list[0]['infoid'])
    

    def get_infoid_per_page(self):
        page_count = self._get_page_count()
        for page in range(0,page_count):
            json = self._get_json(f"https://api2scsou.che168.com/api/v11/search?pageindex={page}&pagesize=1&sort=4&ishideback=1&srecom=2&personalizedpush=1&cid=0&iscxcshowed=-1&scene_no=12&pageid=1757089155_6308&testtype=X&test102223=X&testnewcarspecid=X&test102797=X&otherstatisticsext=%257B%2522history%2522%253A%2522%25E5%2588%2597%25E8%25A1%25A8%25E9%25A1%25B5%2522%252C%2522pvareaid%2522%253A%25220%2522%252C%2522eventid%2522%253A%2522usc_2sc_mc_mclby_cydj_click%2522%257D&filtertype=0&ssnew=1&deviceid=e9adf74b-4f21-4dd6-873f-833e1ea8edba&userid=0&s_pid=0&s_cid=0&_appid=2sc.m&v=11.41.5&_sign=a3ab783193d64735c3f758d4b12fe5bb")
            infoid = self._get_infoid_from_page(json)
            if infoid is None:
                continue
            if self.redis.sismember('infoids', infoid):
                continue
            self.redis.sadd('infoids', infoid)
            publish(infoid)
