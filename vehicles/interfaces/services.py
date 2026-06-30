"""REST API layer for the Vehicles bounded context."""

from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

from vehicles.application.services import (
    AssignInsuranceCommand,
    CarApplicationService,
)
from vehicles.domain.enums import InsuranceType

vehicles_api = Blueprint(
    "vehicles",
    __name__,
    url_prefix="/api/v1/vehicles",
    description="Vehicle catalogue operations",
)

car_service = CarApplicationService()


class VehicleInsuranceSchema(Schema):
    type = fields.Str(metadata={"example": "HIGH_RISK"})
    display_name = fields.Str(metadata={"example": "High risk"})
    annual_rate = fields.Float(metadata={"example": 0.0611})


class VehicleSpecsSchema(Schema):
    engine_power = fields.Str(allow_none=True, metadata={"example": "120 hp"})
    combined_consumption = fields.Str(allow_none=True, metadata={"example": "6.5 L/100km"})
    safety = fields.Str(allow_none=True, metadata={"example": "ABS, airbags"})
    comfort = fields.Str(allow_none=True, metadata={"example": "Air conditioning"})


class VehicleSchema(Schema):
    id = fields.Int(metadata={"example": 1})
    make = fields.Str(metadata={"example": "Toyota"})
    model = fields.Str(metadata={"example": "Corolla"})
    year = fields.Int(metadata={"example": 2023})
    price = fields.Float(metadata={"example": 28500})
    version = fields.Str(allow_none=True, metadata={"example": "XEi"})
    vehicle_type = fields.Str(allow_none=True, metadata={"example": "SEDAN"})
    risk_category = fields.Str(allow_none=True, metadata={"example": "MEDIUM_RISK"})
    reference_price = fields.Float(allow_none=True, metadata={"example": 28500})
    residual_value = fields.Float(allow_none=True, metadata={"example": 9975})
    condition = fields.Str(allow_none=True, metadata={"example": "NEW"})
    fuel_type = fields.Str(allow_none=True, metadata={"example": "Gasoline"})
    transmission = fields.Str(allow_none=True, metadata={"example": "Automatic"})
    mileage = fields.Int(allow_none=True, metadata={"example": 0})
    interest_rate = fields.Str(allow_none=True, metadata={"example": "6.11%"})
    drivetrain = fields.Str(allow_none=True, metadata={"example": "FWD"})
    color_aesthetics = fields.Str(allow_none=True, metadata={"example": "White"})
    specs = fields.Nested(VehicleSpecsSchema)
    photo_url = fields.Url(allow_none=True)
    vehicle_insurance = fields.Nested(VehicleInsuranceSchema, allow_none=True)


class AssignInsuranceRequestSchema(Schema):
    insurance_type = fields.Str(
        required=True,
        metadata={
            "example": "HIGH_RISK",
            "enum": [insurance_type.value for insurance_type in InsuranceType],
        },
    )


class VehicleErrorResponseSchema(Schema):
    error = fields.Str(metadata={"example": "Vehicle not found"})


class AssignInsuranceErrorResponseSchema(VehicleErrorResponseSchema):
    valid_options = fields.List(fields.Str())


@vehicles_api.route("")
class VehicleListResource(MethodView):
    """Return the full vehicle catalogue.

    **Responses:**

    - ``200 OK`` – Body contains a JSON array of all persisted vehicles.

    Returns:
        tuple[flask.Response, int]: A JSON array of vehicle objects paired
        with ``200``.
    """
    @vehicles_api.doc(
        summary="List vehicles",
        description="Returns the full vehicle catalogue.",
        security=[{"bearerAuth": []}],
    )
    @vehicles_api.response(200, VehicleSchema(many=True))
    def get(self):
        cars = car_service.list_cars()
        return [car_service.car_to_dict(car) for car in cars]


@vehicles_api.route("/<int:vehicle_id>")
class VehicleResource(MethodView):
    """Return a single vehicle by id.

    **Responses:**

    - ``200 OK`` – Vehicle found, body contains the vehicle object.
    - ``404 Not Found`` – No vehicle exists with the given ``vehicle_id``.

    Returns:
        tuple[flask.Response, int]: A JSON vehicle object paired with the
        appropriate HTTP status code.
    """
    @vehicles_api.doc(
        summary="Get vehicle by id",
        description="Returns a single vehicle from the catalogue.",
        security=[{"bearerAuth": []}],
    )
    @vehicles_api.response(200, VehicleSchema)
    @vehicles_api.alt_response(404, schema=VehicleErrorResponseSchema, description="Vehicle not found")
    def get(self, vehicle_id):
        car = car_service.get_car(vehicle_id)
        if car is None:
            return {"error": "Vehicle not found"}, 404
        return car_service.car_to_dict(car)


@vehicles_api.route("/<int:vehicle_id>/assign")
class AssignInsuranceResource(MethodView):
    """Assign an insurance type to an existing vehicle.

    **Request body (JSON):**

    .. code-block:: json

        {
            "insurance_type": "HIGH_RISK"
        }

    Valid ``insurance_type`` values: ``LOW_RISK_1``, ``LOW_RISK_2``,
    ``MEDIUM_RISK``, ``HIGH_RISK``, ``PICK_UP``, ``CHINESE_AND_INDIAN``,
    ``L8``, ``OTHERS``.

    **Responses:**

    - ``200 OK`` – Updated vehicle with ``vehicle_insurance`` populated.
    - ``400 Bad Request`` – ``insurance_type`` missing or invalid.
    - ``404 Not Found`` – No vehicle exists with the given ``vehicle_id``.

    Returns:
        tuple[flask.Response, int]: A JSON vehicle object paired with the
        appropriate HTTP status code.
    """
    @vehicles_api.doc(
        summary="Assign insurance",
        description="Assigns an insurance type to an existing vehicle.",
        security=[{"bearerAuth": []}],
    )
    @vehicles_api.arguments(AssignInsuranceRequestSchema)
    @vehicles_api.response(200, VehicleSchema)
    @vehicles_api.alt_response(
        400,
        schema=AssignInsuranceErrorResponseSchema,
        description="Missing or invalid insurance type",
    )
    @vehicles_api.alt_response(404, schema=VehicleErrorResponseSchema, description="Vehicle not found")
    def post(self, data, vehicle_id):
        try:
            car = car_service.assign_insurance(
                AssignInsuranceCommand(vehicle_id, data["insurance_type"])
            )
            return car_service.car_to_dict(car)
        except ValueError as exc:
            if str(exc) == "Car not found":
                return {"error": str(exc)}, 404

            return {
                "error": str(exc),
                "valid_options": [insurance_type.value for insurance_type in InsuranceType],
            }, 400
