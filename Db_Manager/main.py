from models import Cars, TechnicalSpecs, EngineSpecs, TransmissionSpecs, ChassisSpecs, WheelsSpecs, WarrantySpecs
from db_manager import Base, Session, engine
import pika, json, time
from sqlalchemy.inspection import inspect

# Создаём все таблицы
Base.metadata.create_all(bind=engine)

# Списки ключей для каждой связанной таблицы
car_keys = {c.key for c in inspect(Cars).columns}

technical_keys = {
    "car_name_cn", "manufacturer", "vehicle_class", "energy_type", "emission_standard",
    "launch_date", "top_speed_kmh", "acceleration_0_100_kmh_s", "nedc_fuel_consumption",
    "wltc_fuel_consumption", "dimensions_mm", "length_mm", "width_mm", "height_mm",
    "wheelbase_mm", "front_track_mm", "rear_track_mm", "approach_angle_deg", "departure_angle_deg",
    "door_opening", "number_of_doors", "seats", "fuel_tank_capacity_l", "trunk_capacity_l", "curb_weight_kg"
}

engine_keys = {
    "engine_model", "displacement_ml", "displacement_l", "intake_type", "engine_layout",
    "cylinder_arrangement", "cylinders", "valves_per_cylinder", "valve_mechanism",
    "max_horsepower_ps", "max_power_kw", "max_power_rpm", "max_torque_nm", "max_torque_rpm",
    "max_net_power_kw", "engine_technology", "fuel_type", "fuel_grade", "fuel_supply",
    "cylinder_head_material", "engine_block_material"
}

transmission_keys = {"gear_count", "transmission_type", "transmission_short"}
chassis_keys = {"driving_mode", "four_wheel_drive_type", "central_diff_type", "front_suspension",
                "rear_suspension", "steering_assist", "chassis_structure"}
wheels_keys = {"front_brake_type", "rear_brake_type", "parking_brake_type",
               "front_tire_spec", "rear_tire_spec", "spare_tire_spec"}
warranty_keys = {"first_owner_warranty_policy", "vehicle_warranty"}


def connect():
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials)
    )
    channel = connection.channel()
    return connection, channel


def worker(ch, method, properties, body):
    data_dict = json.loads(body.decode())

    # 🔹 Универсальная очистка: "-" / "" / "—" → None
    cleaned_data = {
        k: (None if v in ("-", "", "—") else v)
        for k, v in data_dict.items()
    }

    session = Session()

    try:
        # Сохраняем основной объект Cars
        car_data = {k: cleaned_data[k] for k in car_keys if k in cleaned_data}
        car = Cars(**car_data)

        # Создаём и привязываем нормализованные таблицы, если есть данные
        if any(k in cleaned_data for k in technical_keys):
            tech_data = {k: cleaned_data[k] for k in technical_keys if k in cleaned_data}
            car.technical = TechnicalSpecs(**tech_data)

        if any(k in cleaned_data for k in engine_keys):
            eng_data = {k: cleaned_data[k] for k in engine_keys if k in cleaned_data}
            car.engine = EngineSpecs(**eng_data)

        if any(k in cleaned_data for k in transmission_keys):
            trans_data = {k: cleaned_data[k] for k in transmission_keys if k in cleaned_data}
            car.transmission = TransmissionSpecs(**trans_data)

        if any(k in cleaned_data for k in chassis_keys):
            chassis_data = {k: cleaned_data[k] for k in chassis_keys if k in cleaned_data}
            car.chassis = ChassisSpecs(**chassis_data)

        if any(k in cleaned_data for k in wheels_keys):
            wheels_data = {k: cleaned_data[k] for k in wheels_keys if k in cleaned_data}
            car.wheels = WheelsSpecs(**wheels_data)

        if any(k in cleaned_data for k in warranty_keys):
            warranty_data = {k: cleaned_data[k] for k in warranty_keys if k in cleaned_data}
            car.warranty = WarrantySpecs(**warranty_data)

        # Сохраняем всё сразу
        session.add(car)
        session.commit()
        print(f"✅ Saved car {car.infoid}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        session.rollback()
        print(f"❌ Error while saving car: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    finally:
        session.close()

def consumer():
    connection, channel = connect()
    channel.queue_declare(queue="db_manager", durable=True)
    channel.basic_consume(queue="db_manager", on_message_callback=worker, auto_ack=False)
    try:
        channel.start_consuming()
    except Exception as e:
        print(f"Error {e}")


if __name__ == "__main__":
    time.sleep(60)
    consumer()