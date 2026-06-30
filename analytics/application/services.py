from analytics.domain.algorithms import FrenchMethodAlgorithm
from analytics.domain.entities import PaymentPeriod
from analytics.domain.services import LoanParameterService, LoanFinancialIndicatorsService, PaymentScheduleService, \
    PaymentPeriodService
from analytics.infrastructure.repositories import LoanParametersRepository, LoanFinancialIndicatorsRepository, \
    PaymentScheduleRepository, PaymentPeriodRepository


class PerformFrenchAlgorithmCommand:
    def __init__(
            self,
            user_id: int,
            vehicle_id: int,
            bank_entity: str,
            vehicle_cost: float,
            vehicle_type: str,
            down_payment_percentage: float,
            balloon_payment_percentage: float,
            tea: float,
            initial_payment_date: str,
            total_number_of_years: int,
            grace_period_type: str,
            grace_period_in_months: int = 1,
            period_type: str = "MONTHLY",
    ):
        self.user_id = user_id
        self.vehicle_id = vehicle_id
        self.bank_entity = bank_entity
        self.vehicle_cost = vehicle_cost
        self.vehicle_type = vehicle_type
        self.down_payment_percentage = down_payment_percentage
        self.balloon_payment_percentage = balloon_payment_percentage
        self.tea = tea
        self.initial_payment_date = initial_payment_date
        self.total_number_of_years = total_number_of_years
        self.grace_period_type = grace_period_type
        self.grace_period_in_months = grace_period_in_months
        self.period_type = period_type


class LoanSimulationApplicationService:
    def __init__(self):
        self.loan_parameters_repository = LoanParametersRepository
        self.loan_parameters_service = LoanParameterService
        self.loan_financial_indicators_repository = LoanFinancialIndicatorsRepository
        self.loan_financial_indicators_service = LoanFinancialIndicatorsService
        self.payment_schedule_service = PaymentScheduleService
        self.payment_schedule_repository = PaymentScheduleRepository
        self.payment_period_service = PaymentPeriodService
        self.payment_period_repository = PaymentPeriodRepository

    def perform_french_algorithm(self, command: PerformFrenchAlgorithmCommand) -> dict:

        # Create an instance of the FrenchMethodAlgorithm
        algorithm = FrenchMethodAlgorithm(
            vehicle_cost=command.vehicle_cost,
            vehicle_type=command.vehicle_type,
            down_payment_percentage=command.down_payment_percentage,
            balloon_payment_percentage=command.balloon_payment_percentage,
            tea=command.tea,
            initial_payment_date=command.initial_payment_date,
            total_number_of_years=command.total_number_of_years,
            grace_period_type=command.grace_period_type,
            grace_period_in_months=command.grace_period_in_months,
            period_type=command.period_type,
        )

        # Execute the algorithm
        algorithm.perform()

        # Create a LoanParameters entity
        loan_parameters = self.loan_parameters_service.create(
            bank_entity=command.bank_entity,
            total_years=command.total_number_of_years,
            vehicle_price=command.vehicle_cost,
            vehicle_type=command.vehicle_type,
            down_payment=algorithm.vehicle_cost * algorithm.down_payment_percentage,
            financed_amount=algorithm.financed_amount,
            tea_percentage=command.tea,
            balloon_payment=algorithm.vehicle_cost * algorithm.balloon_payment_percentage,
            grace_period_type=command.grace_period_type,
            grace_period_in_months=command.grace_period_in_months,
            period_type=command.period_type,
            vehicle_id=command.vehicle_id,
            user_id=command.user_id,
        )

        # Persists the loan parameters entity
        loan_parameters = self.loan_parameters_repository.save(loan_parameters)

        # Define a list to hold the payment periods
        payment_periods: list[PaymentPeriod] = []

        # Loop through the payment periods and create PaymentPeriod entities
        for period in algorithm.payment_periods:
            entity = self.payment_period_service.create(
                period_number=period["period"],
                date=period["date"],
                balance_start=period["start"],
                balance_end=period["end"],
                interest=period["interest"],
                amortization=period["amortization"],
                mortgage=period["mortgage"],
                vehicular_insurance=period["vehicular"],
                balloon_fee=period["balloon_fee"],
                total_payment=period["total"],
                net_flow=period["net_flow"],
                grace_period_type=period["grace"]
            )

            # Append the PaymentPeriod entity to the list
            payment_periods.append(entity)

        # Calculate the payment schedule
        payment_schedule = self.payment_schedule_service.create(
            payment_periods,
            loan_parameters.loan_parameters_id,
        )

        # Persists the payment schedule
        payment_schedule = self.payment_schedule_repository.save(payment_schedule)

        # Adds payment schedule id to payment periods
        payment_schedule, payment_periods = self.payment_schedule_service.add_id_to_payment_periods(
            payment_schedule,
            payment_periods
        )

        # Persists all payment periods
        for period in payment_periods:
            self.payment_period_repository.save(period)

        # Calculate financial indicators
        financial_indicators = self.loan_financial_indicators_service.create(
            tcea_percentage=algorithm.tcea,
            van=algorithm.npv,
            tir=algorithm.irr,
            loan_parameters_id=loan_parameters.loan_parameters_id,
        )

        # Persists the financial indicators
        financial_indicators = self.loan_financial_indicators_repository.save(financial_indicators)

        # Return the results
        return {
            "loan_parameters": loan_parameters,
            "payment_schedule": payment_schedule,
            "payment_periods": payment_periods,
            "financial_indicators": financial_indicators,
        }