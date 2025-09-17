import requests
import time

KEY_MAP = {
    # Основные характеристики
    "车型名称": "car_name_cn",
    "厂商": "manufacturer",
    "级别": "vehicle_class",
    "能源类型": "energy_type",
    "环保标准": "emission_standard",
    "发动机": "engine",
    "变速箱": "transmission",
    "车身结构": "body_structure",
    "驱动方式": "driving_mode",

    # Гарантии
    "首任车主质保政策": "first_owner_warranty_policy",
    "整车质保": "vehicle_warranty",

    # Даты и показатели
    "上市时间": "launch_date",
    "最高车速(km/h)": "top_speed_kmh",
    "官方0-100km/h加速(s)": "acceleration_0_100_kmh_s",
    "NEDC综合油耗(L/100km)": "nedc_fuel_consumption",
    "WLTC综合油耗(L/100km)": "wltc_fuel_consumption",

    # Размеры
    "长*宽*高(mm)": "dimensions_mm",
    "长度(mm)": "length_mm",
    "宽度(mm)": "width_mm",
    "高度(mm)": "height_mm",
    "轴距(mm)": "wheelbase_mm",
    "前轮距(mm)": "front_track_mm",
    "后轮距(mm)": "rear_track_mm",
    "接近角(°)": "approach_angle_deg",
    "离去角(°)": "departure_angle_deg",
    "车门开启方式": "door_opening",
    "车门数(个)": "number_of_doors",
    "座位数(个)": "seats",
    "油箱容积(L)": "fuel_tank_capacity_l",
    "后备厢容积(L)": "trunk_capacity_l",
    "整备质量(kg)": "curb_weight_kg",

    # Двигатель
    "发动机型号": "engine_model",
    "排量(mL)": "displacement_ml",
    "排量(L)": "displacement_l",
    "进气形式": "intake_type",
    "发动机布局": "engine_layout",
    "气缸排列形式": "cylinder_arrangement",
    "气缸数(个)": "cylinders",
    "每缸气门数(个)": "valves_per_cylinder",
    "配气机构": "valve_mechanism",
    "最大马力(Ps)": "max_horsepower_ps",
    "最大功率(kW)": "max_power_kw",
    "最大功率转速(rpm)": "max_power_rpm",
    "最大扭矩(N・m)": "max_torque_nm",
    "最大扭矩转速(rpm)": "max_torque_rpm",
    "最大净功率(kW)": "max_net_power_kw",
    "发动机特有技术": "engine_technology",
    "燃料形式": "fuel_type",
    "燃油标号": "fuel_grade",
    "供油方式": "fuel_supply",
    "缸盖材料": "cylinder_head_material",
    "缸体材料": "engine_block_material",

    # Коробка передач
    "挡位个数": "gear_count",
    "变速箱类型": "transmission_type",
    "简称": "transmission_short",

    # Подвеска и привод
    "四驱形式": "four_wheel_drive_type",
    "中央差速器结构": "central_diff_type",
    "前悬架类型": "front_suspension",
    "后悬架类型": "rear_suspension",
    "助力类型": "steering_assist",
    "车体结构": "chassis_structure",

    # Тормоза и колеса
    "前制动器类型": "front_brake_type",
    "后制动器类型": "rear_brake_type",
    "驻车制动类型": "parking_brake_type",
    "前轮胎规格": "front_tire_spec",
    "后轮胎规格": "rear_tire_spec",
    "备胎规格": "spare_tire_spec",
}

class Translator:
    def __init__(self):
        self.api_key = "Api-Key"
        self.url = "https://api.nbrb.by/exrates/rates/CNY?parammode=2"

    def _translate_text(self, text, target_language, source_language="zh"):
        body = {
            "targetLanguageCode": target_language,
            "sourceLanguageCode": source_language,
            "texts": [text],
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}",
        }
        response = requests.post(
            "https://translate.api.cloud.yandex.net/translate/v2/translate",
            json=body,
            headers=headers,
            timeout=600,
        )
        response.raise_for_status()
        data = response.json()
        return data["translations"][0]["text"]

    def _get_price(self, price):
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        data = response.json()
        value = data["Cur_OfficialRate"] / data["Cur_Scale"]

        price_in_cny = price * 10000
        price_in_byn = price_in_cny * value
        return round(price_in_byn, 2)

    def translator(self, data):
        en_fields = [
                        "carname",
                        "brandname",
                        "seriesname",
                        "车型名称",       # car_name_cn
                        "厂商",          # manufacturer
                        "级别",          # vehicle_class
                        "能源类型",       # energy_type
                        "环保标准",       # emission_standard
                        "发动机",        # engine
                        "变速箱",        # transmission
                        "车身结构",       # body_structure
                        "驱动方式",       # driving_mode
                        "上市时间",       # launch_date
                        "最高车速(km/h)",  # top_speed_kmh
                        "官方0-100km/h加速(s)",  # acceleration_0_100_kmh_s
                        "NEDC综合油耗(L/100km)",  # nedc_fuel_consumption
                        "WLTC综合油耗(L/100km)",  # wltc_fuel_consumption
                        "长*宽*高(mm)",    # dimensions_mm
                        "长度(mm)",       # length_mm
                        "宽度(mm)",       # width_mm
                        "高度(mm)",       # height_mm
                        "轴距(mm)",       # wheelbase_mm
                        "前轮距(mm)",     # front_track_mm
                        "后轮距(mm)",     # rear_track_mm
                        "接近角(°)",      # approach_angle_deg
                        "离去角(°)",      # departure_angle_deg
                        "车门开启方式",     # door_opening
                        "车门数(个)",      # number_of_doors
                        "座位数(个)",      # seats
                        "油箱容积(L)",     # fuel_tank_capacity_l
                        "后备厢容积(L)",    # trunk_capacity_l
                        "整备质量(kg)",     # curb_weight_kg
                        "发动机型号",      # engine_model
                        "排量(mL)",       # displacement_ml
                        "排量(L)",        # displacement_l
                        "进气形式",       # intake_type
                        "发动机布局",      # engine_layout
                        "气缸排列形式",     # cylinder_arrangement
                        "气缸数(个)",      # cylinders
                        "每缸气门数(个)",   # valves_per_cylinder
                        "配气机构",       # valve_mechanism
                        "最大马力(Ps)",    # max_horsepower_ps
                        "最大功率(kW)",    # max_power_kw
                        "最大功率转速(rpm)",  # max_power_rpm
                        "最大扭矩(N・m)",   # max_torque_nm
                        "最大扭矩转速(rpm)",  # max_torque_rpm
                        "最大净功率(kW)",   # max_net_power_kw
                        "发动机特有技术",    # engine_technology
                        "燃料形式",       # fuel_type
                        "燃油标号",       # fuel_grade
                        "供油方式",       # fuel_supply
                        "缸盖材料",       # cylinder_head_material
                        "缸体材料",       # engine_block_material
                        "挡位个数",       # gear_count
                        "变速箱类型",      # transmission_type
                        "简称",          # transmission_short
                        "四驱形式",       # four_wheel_drive_type
                        "中央差速器结构",    # central_diff_type
                        "前悬架类型",      # front_suspension
                        "后悬架类型",      # rear_suspension
                        "助力类型",       # steering_assist
                        "车体结构",       # chassis_structure
                        "前制动器类型",     # front_brake_type
                        "后制动器类型",     # rear_brake_type
                        "驻车制动类型",     # parking_brake_type
                        "前轮胎规格",      # front_tire_spec
                        "后轮胎规格",      # rear_tire_spec
                        "备胎规格",       # spare_tire_spec
                    ]

        ru_fields = [
                        "colorname",
                        "gearbox",
                        "drivingmode",
                        "remark",
                        "首任车主质保政策",  # first_owner_warranty_policy
                        "整车质保",       # vehicle_warranty
                    ]

        price_fields = [
                        "price",
                        "guidanceprice"
                    ]

        for field, value in list(data.items()):
            if value is None or (isinstance(value, str) and not value.strip()):
                print(f"{field} is None or empty")
                continue

            if field in en_fields:
                data[field] = self._translate_text(str(value), "en")
            elif field in ru_fields:
                data[field] = self._translate_text(str(value), "ru")
            elif field in price_fields:
                try:
                    data[field] = self._get_price(float(value))
                except ValueError:
                    print(f"Cannot convert {field}='{value}' to float for price conversion")

        for old_key, new_key in KEY_MAP.items():
            if old_key in data:
                data[new_key] = data.pop(old_key)
        print(data)
        return data