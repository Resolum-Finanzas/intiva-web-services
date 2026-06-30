"""Interface (REST API) layer for the Vehicles bounded context.

Exposes a Flask Blueprint (``vehicles_api``) that translates incoming HTTP
requests into calls to the application service and maps the results back to
JSON responses.  This layer owns no domain logic; it is responsible solely
for I/O concerns: parsing request data and HTTP status code selection.

Vehicles are seeded at application startup via
``vehicles.application.services.on_application_started``, so this layer
exposes no creation endpoint — only read access and insurance assignment.
"""

from flask import Blueprint, request, jsonify

from vehicles.application.services import (
    CarApplicationService,
    AssignInsuranceCommand,
)
from vehicles.domain.enums import InsuranceType

vehicles_api = Blueprint("vehicles_api", __name__)

# Module-level singleton; safe because Flask handles one request at a time
# within a single worker (no shared mutable state on this object).
car_service = CarApplicationService()


@vehicles_api.route("/api/v1/vehicles", methods=["GET"])
def list_vehicles():
    """Return the full vehicle catalogue.

    **Responses:**

    - ``200 OK`` – Body contains a JSON array of all persisted vehicles.

    Returns:
        tuple[flask.Response, int]: A JSON array of vehicle objects paired
        with ``200``.
    """
    cars = car_service.list_cars()
    return jsonify([car_service.car_to_dict(c) for c in cars]), 200


@vehicles_api.route("/api/v1/vehicles/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    """Return a single vehicle by id.

    **Responses:**

    - ``200 OK`` – Vehicle found, body contains the vehicle object.
    - ``404 Not Found`` – No vehicle exists with the given ``vehicle_id``.

    Returns:
        tuple[flask.Response, int]: A JSON vehicle object paired with the
        appropriate HTTP status code.
    """
    car = car_service.get_car(vehicle_id)
    if car is None:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(car_service.car_to_dict(car)), 200


@vehicles_api.route("/api/v1/vehicles/<int:vehicle_id>/assign", methods=["POST"])
def assign_insurance(vehicle_id):
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
    data = request.get_json(silent=True) or {}  
    try:
        insurance_type = data["insurance_type"]
        car = car_service.assign_insurance(
            AssignInsuranceCommand(vehicle_id, insurance_type)
        )
        return jsonify(car_service.car_to_dict(car)), 200
    except KeyError:
        return jsonify({
            "error": "insurance_type is required",
            "valid_options": [t.value for t in InsuranceType],
        }), 400
    except ValueError as e:
        status = 404 if str(e) == "Car not found" else 400
        return jsonify({"error": str(e)}), status