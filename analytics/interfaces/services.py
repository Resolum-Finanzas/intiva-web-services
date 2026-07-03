from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

from analytics.application.services import (
    LoanSimulationApplicationService,
    PerformFrenchAlgorithmCommand,
)

analytics_api = Blueprint(
    "analytics",
    __name__,
    url_prefix="/api/v1/analytics",
    description="Analytics operations"
)

load_simulator_service = LoanSimulationApplicationService()


def serialize_payment_period(period) -> dict:
    return {
        "payment_period_id": period.payment_period_id,
        "period_number": period.period_number,
        "payment_date": period.payment_date,
        "balance_start": period.balance_start,
        "balance_end": period.balance_end,
        "interest": period.interest,
        "amortization": period.amortization,
        "french_installment": period.french_installment,
        "mortgage": period.mortgage,
        "vehicular_insurance": period.vehicular_insurance,
        "balloon_fee": period.balloon_fee,
        "total_payment": period.total_payment,
        "net_flow": period.net_flow,
        "grace_period_type": period.grace_period_type,
        "payment_schedule_id": period.payment_schedule_id,
    }


def serialize_payment_schedule(schedule) -> dict:
    return {
        "payment_schedule_id": schedule.payment_schedule_id,
        "loan_parameters_id": schedule.loan_parameters_id,
        "total_interest": schedule.total_interest,
        "total_amortization": schedule.total_amortization,
        "total_mortgage_protection_insurance": schedule.total_mortgage_protection_insurance,
        "total_vehicular_insurance": schedule.total_vehicular_insurance,
        "total_payment": schedule.total_payment,
        "payment_periods": [
            serialize_payment_period(period)
            for period in schedule.payment_periods
        ],
    }


class LoanSimulationErrorResponseSchema(Schema):
    error = fields.Str(metadata={"example": "Vehicle not found"})


class LoanSimulationRequestSchema(Schema):
    user_id = fields.Int(required=True)
    vehicle_id = fields.Int(required=True)
    bank_entity = fields.Str(required=True)
    vehicle_cost = fields.Float(required=True)
    down_payment_percentage = fields.Float(required=True)
    balloon_payment_percentage = fields.Float(required=True)
    tea = fields.Float(required=True)
    initial_payment_date = fields.Str(required=True)
    total_number_of_years = fields.Int(required=True)
    grace_period_type = fields.Str(required=True)
    grace_period_in_months = fields.Int(load_default=0)
    period_type = fields.Str(load_default="MONTHLY")


@analytics_api.route("/loan-simulation")
class LoanSimulationResource(MethodView):

    @analytics_api.doc(
        summary="Perform loan simulation",
        description="Executes the French method algorithm for smart purchase loan simulation.",
        security=[{"bearerAuth": []}],
    )
    @analytics_api.arguments(LoanSimulationRequestSchema)
    @analytics_api.response(201)
    @analytics_api.alt_response(404, schema=LoanSimulationErrorResponseSchema, description="Vehicle not found")
    def post(self, data):
        command = PerformFrenchAlgorithmCommand(
            user_id=data["user_id"],
            vehicle_id=data["vehicle_id"],
            bank_entity=data["bank_entity"],
            vehicle_cost=data["vehicle_cost"],
            down_payment_percentage=data["down_payment_percentage"],
            balloon_payment_percentage=data["balloon_payment_percentage"],
            tea=data["tea"],
            initial_payment_date=data["initial_payment_date"],
            total_number_of_years=data["total_number_of_years"],
            grace_period_type=data["grace_period_type"],
            grace_period_in_months=data.get("grace_period_in_months", 0),
            period_type=data.get("period_type", "MONTHLY"),
        )

        try:
            result = load_simulator_service.perform_french_algorithm(command)
        except ValueError as exc:
            return {"error": str(exc)}, 404

        return {
            "loan_parameters": result["loan_parameters"].__dict__,
            "payment_schedule": serialize_payment_schedule(result["payment_schedule"]),
            "payment_periods": [
                serialize_payment_period(period)
                for period in result["payment_periods"]
            ],
            "financial_indicators": result["financial_indicators"].__dict__,
        }
