import requests
import re
import json

class CarDetail:
    def __init__(self):
        
        self.url = 'https://apiuscdt.che168.com/apic/v2/car/getcarinfo'

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


    def _get_json(self, infoid):
        self.params = {
                        "infoid": infoid,
                        "deviceid": "e9adf74b-4f21-4dd6-873f-833e1ea8edba",
                        "ucuserauth": "",
                        "gpscid": "0",
                        "iscardetailab": "B",
                        "encryptinfo": "",
                        "fromtag": "0",
                        "pvareaid": "108948",
                        "userid": "0",
                        "s_pid": "0",
                        "s_cid": "0",
                        "_appid": "2sc.m",
                        "v": "11.41.5",
                        }
        response = self.session.get(self.url, params =  self.params)
        return response.json()
    

    def get_car_detaile(self, infoid):
        json_data = self._get_json(infoid)
        
        data = {
            "infoid": json_data['result'].get("infoid"),
            "carname": json_data['result'].get("carname"),
            "brandname": json_data['result'].get("brandname"),
            "seriesname": json_data['result'].get("seriesname"),
            "colorname": json_data['result'].get("colorname"),
            "remark": json_data['result'].get("remark"),
            "price": float(json_data['result'].get("price", 0)),
            "firstregyear": str(json_data['result'].get("firstregyear", "")),
            "guidanceprice": float(json_data['result'].get("guidanceprice", 0)),
            "displacement": float(json_data['result'].get("displacement", 0)),
            "gearbox": json_data['result'].get("gearbox"),
            "drivingmode": json_data['result'].get("drivingmode"),
            "mileage": float(json_data['result'].get("mileage", 0)) * 10000,
            "main_image": json_data['result'].get("imageurl"),
            "images": json_data['result'].get("piclist", []),
            "specid": json_data['result'].get("specid"),
        }

        # Получаем spec параметры
        specid = data["specid"]
        if specid:
            url = f"https://cacheapigo.che168.com/CarProduct/GetParam.ashx?specid={specid}&callback=configTitle"
            response = requests.get(url)
            raw_text = response.text.strip()
            clean_text = re.sub(r'^configTitle\(|\)$', '', raw_text)
            spec_data = json.loads(clean_text)

            
            param_items = spec_data.get("result", {}).get("paramtypeitems", [])
            for paramtype in param_items:
                for item in paramtype.get("paramitems", []):
                    key = item.get("name")      
                    value = item.get("value")  
                    if key:
                        data[key] = value
        print(data)
        return data
    
if __name__ == '__main__':
    car = CarDetail()
    car.get_car_detaile(56115935)
