from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String, Integer, ForeignKey
from db_manager import Base

class Cars(Base):
    __tablename__ = "cars"

    infoid: Mapped[int] = mapped_column(Integer, primary_key=True)
    carname: Mapped[str] = mapped_column(String, nullable=True)
    brandname: Mapped[str] = mapped_column(String, nullable=True)
    seriesname: Mapped[str] = mapped_column(String, nullable=True)
    colorname: Mapped[str] = mapped_column(String, nullable=True)
    remark: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[str] = mapped_column(String, nullable=True)
    firstregyear: Mapped[str] = mapped_column(String, nullable=True)
    guidanceprice: Mapped[str] = mapped_column(String, nullable=True)
    displacement: Mapped[str] = mapped_column(String, nullable=True)
    gearbox: Mapped[str] = mapped_column(String, nullable=True)
    drivingmode: Mapped[str] = mapped_column(String, nullable=True)
    mileage: Mapped[str] = mapped_column(String, nullable=True)
    main_image: Mapped[str] = mapped_column(String, nullable=True)
    images: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)

    technical: Mapped["TechnicalSpecs"] = relationship("TechnicalSpecs", uselist=False, back_populates="car")
    engine: Mapped["EngineSpecs"] = relationship("EngineSpecs", uselist=False, back_populates="car")
    transmission: Mapped["TransmissionSpecs"] = relationship("TransmissionSpecs", uselist=False, back_populates="car")
    chassis: Mapped["ChassisSpecs"] = relationship("ChassisSpecs", uselist=False, back_populates="car")
    wheels: Mapped["WheelsSpecs"] = relationship("WheelsSpecs", uselist=False, back_populates="car")
    warranty: Mapped["WarrantySpecs"] = relationship("WarrantySpecs", uselist=False, back_populates="car")


class TechnicalSpecs(Base):
    __tablename__ = "technical_specs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.infoid"))

    car_name_cn: Mapped[str] = mapped_column(String, nullable=True)
    manufacturer: Mapped[str] = mapped_column(String, nullable=True)
    vehicle_class: Mapped[str] = mapped_column(String, nullable=True)
    energy_type: Mapped[str] = mapped_column(String, nullable=True)
    emission_standard: Mapped[str] = mapped_column(String, nullable=True)
    launch_date: Mapped[str] = mapped_column(String, nullable=True)
    top_speed_kmh: Mapped[str] = mapped_column(String, nullable=True)
    acceleration_0_100_kmh_s: Mapped[str] = mapped_column(String, nullable=True)
    nedc_fuel_consumption: Mapped[str] = mapped_column(String, nullable=True)
    wltc_fuel_consumption: Mapped[str] = mapped_column(String, nullable=True)
    dimensions_mm: Mapped[str] = mapped_column(String, nullable=True)
    length_mm: Mapped[str] = mapped_column(String, nullable=True)
    width_mm: Mapped[str] = mapped_column(String, nullable=True)
    height_mm: Mapped[str] = mapped_column(String, nullable=True)
    wheelbase_mm: Mapped[str] = mapped_column(String, nullable=True)
    front_track_mm: Mapped[str] = mapped_column(String, nullable=True)
    rear_track_mm: Mapped[str] = mapped_column(String, nullable=True)
    approach_angle_deg: Mapped[str] = mapped_column(String, nullable=True)
    departure_angle_deg: Mapped[str] = mapped_column(String, nullable=True)
    door_opening: Mapped[str] = mapped_column(String, nullable=True)
    number_of_doors: Mapped[str] = mapped_column(String, nullable=True)
    seats: Mapped[str] = mapped_column(String, nullable=True)
    fuel_tank_capacity_l: Mapped[str] = mapped_column(String, nullable=True)
    trunk_capacity_l: Mapped[str] = mapped_column(String, nullable=True)
    curb_weight_kg: Mapped[str] = mapped_column(String, nullable=True)

    car: Mapped["Cars"] = relationship("Cars", back_populates="technical")


class EngineSpecs(Base):
    __tablename__ = "engine_specs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    car_id: Mapped[int] = mapped_column(ForeignKey("cars.infoid"))

    engine_model: Mapped[str] = mapped_column(String, nullable=True)
    displacement_ml: Mapped[str] = mapped_column(String, nullable=True)
    displacement_l: Mapped[str] = mapped_column(String, nullable=True)
    intake_type: Mapped[str] = mapped_column(String, nullable=True)
    engine_layout: Mapped[str] = mapped_column(String, nullable=True)
    cylinder_arrangement: Mapped[str] = mapped_column(String, nullable=True)
    cylinders: Mapped[str] = mapped_column(String, nullable=True)
    valves_per_cylinder: Mapped[str] = mapped_column(String, nullable=True)
    valve_mechanism: Mapped[str] = mapped_column(String, nullable=True)
    max_horsepower_ps: Mapped[str] = mapped_column(String, nullable=True)
    max_power_kw: Mapped[str] = mapped_column(String, nullable=True)
    max_power_rpm: Mapped[str] = mapped_column(String, nullable=True)
    max_torque_nm: Mapped[str] = mapped_column(String, nullable=True)
    max_torque_rpm: Mapped[str] = mapped_column(String, nullable=True)
    max_net_power_kw: Mapped[str] = mapped_column(String, nullable=True)
    engine_technology: Mapped[str] = mapped_column(String, nullable=True)
    fuel_type: Mapped[str] = mapped_column(String, nullable=True)
    fuel_grade: Mapped[str] = mapped_column(String, nullable=True)
    fuel_supply: Mapped[str] = mapped_column(String, nullable=True)
    cylinder_head_material: Mapped[str] = mapped_column(String, nullable=True)
    engine_block_material: Mapped[str] = mapped_column(String, nullable=True)

    car: Mapped["Cars"] = relationship("Cars", back_populates="engine")


class TransmissionSpecs(Base):
    __tablename__ = "transmission_specs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.infoid"))

    gear_count: Mapped[str] = mapped_column(String, nullable=True)
    transmission_type: Mapped[str] = mapped_column(String, nullable=True)
    transmission_short: Mapped[str] = mapped_column(String, nullable=True)

    car: Mapped["Cars"] = relationship("Cars", back_populates="transmission")


class ChassisSpecs(Base):
    __tablename__ = "chassis_specs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.infoid"))

    driving_mode: Mapped[str] = mapped_column(String, nullable=True)
    four_wheel_drive_type: Mapped[str] = mapped_column(String, nullable=True)
    central_diff_type: Mapped[str] = mapped_column(String, nullable=True)
    front_suspension: Mapped[str] = mapped_column(String, nullable=True)
    rear_suspension: Mapped[str] = mapped_column(String, nullable=True)
    steering_assist: Mapped[str] = mapped_column(String, nullable=True)
    chassis_structure: Mapped[str] = mapped_column(String, nullable=True)

    car: Mapped["Cars"] = relationship("Cars", back_populates="chassis")


class WheelsSpecs(Base):
    __tablename__ = "wheels_specs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.infoid"))

    front_brake_type: Mapped[str] = mapped_column(String, nullable=True)
    rear_brake_type: Mapped[str] = mapped_column(String, nullable=True)
    parking_brake_type: Mapped[str] = mapped_column(String, nullable=True)
    front_tire_spec: Mapped[str] = mapped_column(String, nullable=True)
    rear_tire_spec: Mapped[str] = mapped_column(String, nullable=True)
    spare_tire_spec: Mapped[str] = mapped_column(String, nullable=True)

    car: Mapped["Cars"] = relationship("Cars", back_populates="wheels")


class WarrantySpecs(Base):
    __tablename__ = "warranty_specs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.infoid"))

    first_owner_warranty_policy: Mapped[str] = mapped_column(String, nullable=True)
    vehicle_warranty: Mapped[str] = mapped_column(String, nullable=True)

    car: Mapped["Cars"] = relationship("Cars", back_populates="warranty")