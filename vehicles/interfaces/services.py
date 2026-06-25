"""Interface (REST API) layer for the Vehicles bounded context.

Exposes a Flask Blueprint (``vehicles_api``) that translates incoming HTTP
requests into calls to the application service and maps the results back to
JSON responses.  This layer owns no domain logic; it is responsible solely
for I/O concerns: parsing request data and HTTP status code selection.
"""

from flask import Blueprint, jsonify, request

from vehicles.application.services import CarApplicationService, CreateCarCommand

vehicles_api = Blueprint("vehicles_api", __name__)

# Module-level singleton; safe because Flask handles one request at a time
# within a single worker (no shared mutable state on this object).
_service = CarApplicationService()


@vehicles_api.route("/api/v1/vehicles/cars", methods=["GET"])
def list_cars():
    """Return the full car catalogue.

    **Responses:**

    - ``200 OK`` — Body contains a JSON array of all persisted cars.  An
      empty catalogue returns an empty array (not a 404).

    Returns:
        tuple[flask.Response, int]: A JSON array of car objects paired with
        ``200``.
    """
    cars = _service.list_cars()
    return jsonify([
        {
            "id": c.id,
            "make": c.make,
            "model": c.model,
            "year": c.year,
            "price": c.price,
            "photo_url": c.photo_url,
        }
        for c in cars
    ]), 200


@vehicles_api.route("/api/v1/vehicles/cars", methods=["POST"])
def create_car():
    """Create a new car listing.

    Accepts a ``multipart/form-data`` request so that a cover photo can be
    attached alongside the structured fields.

    **Request body (multipart/form-data):**

    - ``make`` *(str, required)*: Manufacturer name.
    - ``model`` *(str, required)*: Model designation.
    - ``year`` *(int, required)*: Production year.
    - ``price`` *(float, required)*: Listed sale price.
    - ``image`` *(file, optional)*: Cover photo for the listing.

    **Responses:**

    - ``201 Created`` — Car saved successfully.  Body contains the persisted
      record with its assigned ``id`` and resolved ``photo_url``.
    - ``400 Bad Request`` — A required field is missing or a domain invariant
      is violated (e.g. year out of range, negative price).

    Returns:
        tuple[flask.Response, int]: A JSON car object paired with the
        appropriate HTTP status code.
    """
    if not request.form.get("make") or not request.form.get("model") \
            or not request.form.get("year") or not request.form.get("price"):
        return jsonify({"error": "make, model, year and price are required"}), 400

    image_data: bytes | None = None
    if "image" in request.files:
        image_data = request.files["image"].read()

    try:
        car = _service.create_car(CreateCarCommand(
            make=request.form["make"],
            model=request.form["model"],
            year=int(request.form["year"]), 
            price=float(request.form["price"]),
            image_data=image_data,
        ))
        return jsonify({
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "price": car.price,
            "photo_url": car.photo_url,
        }), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
