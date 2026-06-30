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


class LoanSimulationRequestSchema(Schema):
    user_id = fields.Int(required=True)
    vehicle_id = fields.Int(required=True)
    bank_entity = fields.Str(required=True)
    vehicle_cost = fields.Float(required=True)
    vehicle_type = fields.Str(required=True)
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
    def post(self, data):
        command = PerformFrenchAlgorithmCommand(
            user_id=data["user_id"],
            vehicle_id=data["vehicle_id"],
            bank_entity=data["bank_entity"],
            vehicle_cost=data["vehicle_cost"],
            vehicle_type=data["vehicle_type"],
            down_payment_percentage=data["down_payment_percentage"],
            balloon_payment_percentage=data["balloon_payment_percentage"],
            tea=data["tea"],
            initial_payment_date=data["initial_payment_date"],
            total_number_of_years=data["total_number_of_years"],
            grace_period_type=data["grace_period_type"],
            grace_period_in_months=data.get("grace_period_in_months", 0),
            period_type=data.get("period_type", "MONTHLY"),
        )

        result = load_simulator_service.perform_french_algorithm(command)

        return {
            "loan_parameters": result["loan_parameters"].__dict__,
            "payment_schedule": result["payment_schedule"].__dict__,
            "payment_periods": [
                period.__dict__ for period in result["payment_periods"]
            ],
            "financial_indicators": result["financial_indicators"].__dict__,
        }
