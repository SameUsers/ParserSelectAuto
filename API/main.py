from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models import Cars, TechnicalSpecs, EngineSpecs, TransmissionSpecs, ChassisSpecs, WheelsSpecs, WarrantySpecs
from db_manager import Session as SessionLocal, Base, engine
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Car API")

# Pydantic схемы
class BaseSpecsSchema(BaseModel):
    class Config:
        orm_mode = True

class TechnicalSpecsSchema(BaseSpecsSchema):
    car_name_cn: Optional[str]
    manufacturer: Optional[str]
    vehicle_class: Optional[str]
    energy_type: Optional[str]
    emission_standard: Optional[str]
    launch_date: Optional[str]
    top_speed_kmh: Optional[str]
    acceleration_0_100_kmh_s: Optional[str]
    nedc_fuel_consumption: Optional[str]
    wltc_fuel_consumption: Optional[str]
    dimensions_mm: Optional[str]
    length_mm: Optional[str]
    width_mm: Optional[str]
    height_mm: Optional[str]
    wheelbase_mm: Optional[str]
    front_track_mm: Optional[str]
    rear_track_mm: Optional[str]
    approach_angle_deg: Optional[str]
    departure_angle_deg: Optional[str]
    door_opening: Optional[str]
    number_of_doors: Optional[str]
    seats: Optional[str]
    fuel_tank_capacity_l: Optional[str]
    trunk_capacity_l: Optional[str]
    curb_weight_kg: Optional[str]

class EngineSpecsSchema(BaseSpecsSchema):
    engine_model: Optional[str]
    displacement_ml: Optional[str]
    displacement_l: Optional[str]
    intake_type: Optional[str]
    engine_layout: Optional[str]
    cylinder_arrangement: Optional[str]
    cylinders: Optional[str]
    valves_per_cylinder: Optional[str]
    valve_mechanism: Optional[str]
    max_horsepower_ps: Optional[str]
    max_power_kw: Optional[str]
    max_power_rpm: Optional[str]
    max_torque_nm: Optional[str]
    max_torque_rpm: Optional[str]
    max_net_power_kw: Optional[str]
    engine_technology: Optional[str]
    fuel_type: Optional[str]
    fuel_grade: Optional[str]
    fuel_supply: Optional[str]
    cylinder_head_material: Optional[str]
    engine_block_material: Optional[str]

class TransmissionSpecsSchema(BaseSpecsSchema):
    gear_count: Optional[str]
    transmission_type: Optional[str]
    transmission_short: Optional[str]

class ChassisSpecsSchema(BaseSpecsSchema):
    driving_mode: Optional[str]
    four_wheel_drive_type: Optional[str]
    central_diff_type: Optional[str]
    front_suspension: Optional[str]
    rear_suspension: Optional[str]
    steering_assist: Optional[str]
    chassis_structure: Optional[str]

class WheelsSpecsSchema(BaseSpecsSchema):
    front_brake_type: Optional[str]
    rear_brake_type: Optional[str]
    parking_brake_type: Optional[str]
    front_tire_spec: Optional[str]
    rear_tire_spec: Optional[str]
    spare_tire_spec: Optional[str]

class WarrantySpecsSchema(BaseSpecsSchema):
    first_owner_warranty_policy: Optional[str]
    vehicle_warranty: Optional[str]

class CarSchema(BaseSpecsSchema):
    infoid: int
    carname: Optional[str]
    brandname: Optional[str]
    seriesname: Optional[str]
    colorname: Optional[str]
    remark: Optional[str]
    price: Optional[str]
    firstregyear: Optional[str]
    guidanceprice: Optional[str]
    displacement: Optional[str]
    gearbox: Optional[str]
    drivingmode: Optional[str]
    mileage: Optional[str]
    main_image: Optional[str]
    images: Optional[List[str]]

    technical: Optional[TechnicalSpecsSchema]
    engine: Optional[EngineSpecsSchema]
    transmission: Optional[TransmissionSpecsSchema]
    chassis: Optional[ChassisSpecsSchema]
    wheels: Optional[WheelsSpecsSchema]
    warranty: Optional[WarrantySpecsSchema]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/cars", response_model=List[CarSchema])
def get_cars(
    offset: int = 0,
    limit: int = 20,
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to include"),

    # --- фильтры ---
    brandname: Optional[str] = None,
    seriesname: Optional[str] = None,
    firstregyear: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    vehicle_class: Optional[str] = None,
    energy_type: Optional[str] = None,

    db: Session = Depends(get_db)
):
    query = db.query(Cars).options(
        joinedload(Cars.technical),
        joinedload(Cars.engine),
        joinedload(Cars.transmission),
        joinedload(Cars.chassis),
        joinedload(Cars.wheels),
        joinedload(Cars.warranty)
    )

    # --- динамическая фильтрация ---
    filters = []
    if brandname:
        filters.append(Cars.brandname.ilike(f"%{brandname}%"))
    if seriesname:
        filters.append(Cars.seriesname.ilike(f"%{seriesname}%"))
    if firstregyear:
        filters.append(Cars.firstregyear.ilike(f"%{firstregyear}%"))
    if min_price:
        filters.append(Cars.price >= min_price)
    if max_price:
        filters.append(Cars.price <= max_price)
    if vehicle_class:
        query = query.join(TechnicalSpecs)
        filters.append(TechnicalSpecs.vehicle_class.ilike(f"%{vehicle_class}%"))
    if energy_type:
        query = query.join(TechnicalSpecs)
        filters.append(TechnicalSpecs.energy_type.ilike(f"%{energy_type}%"))

    if filters:
        query = query.filter(and_(*filters))

    # Пагинация
    query = query.offset(offset).limit(limit)
    cars = query.all()

    if fields:
        field_set = set(f.strip() for f in fields.split(","))
        filtered_cars = []
        for car in cars:
            filtered = {k: v for k, v in car.__dict__.items() if k in field_set or k.startswith("_")}
            filtered_cars.append(filtered)
        return filtered_cars

    return cars


@app.get("/car/{car_id}", response_model=CarSchema)
def get_car(
    car_id: int,
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to include"),
    db: Session = Depends(get_db)
):
    car = db.query(Cars).options(
        joinedload(Cars.technical),
        joinedload(Cars.engine),
        joinedload(Cars.transmission),
        joinedload(Cars.chassis),
        joinedload(Cars.wheels),
        joinedload(Cars.warranty)
    ).filter(Cars.infoid == car_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if fields:
        field_set = set(f.strip() for f in fields.split(","))
        filtered = {k: v for k, v in car.__dict__.items() if k in field_set or k.startswith("_")}
        return filtered

    return car