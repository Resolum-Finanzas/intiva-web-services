from datetime import datetime

from analytics.domain.entities import LoanParameters, LoanFinancialIndicators, PaymentPeriod, PaymentSchedule


class LoanParameterService:
    @staticmethod
    def create(
            bank_entity: str,
            total_years: int,
            vehicle_price: float,
            vehicle_type: str,
            down_payment: float,
            financed_amount: float,
            tea_percentage: float,
            balloon_payment: float,
            grace_period_type: str,
            grace_period_in_months: int,
            vehicle_id: int,
            user_id: int,
            period_type: str = "MONTHLY",
    ) -> LoanParameters:
        """ Create a new LoanParameters instance. """

        try:
            vehicle_price = float(vehicle_price)
            if vehicle_price <= 0:
                raise ValueError("Vehicle price must be greater than 0")

            down_payment_percentage = float(down_payment)
            if down_payment_percentage < 0:
                raise ValueError("Down payment must be greater than 0")

            financed_amount = float(financed_amount)
            if financed_amount <= 0:
                raise ValueError("Financed amount must be greater than 0")

            tea_percentage = float(tea_percentage)
            if tea_percentage < 0 or tea_percentage > 1:
                raise ValueError("TEA percentage must be between 0 and 1")

            balloon_payment = float(balloon_payment)
            if balloon_payment < 0:
                raise ValueError("Balloon payment must be greater 0")

            grace_period_in_months = int(grace_period_in_months)
            if grace_period_in_months < 0:
                raise ValueError("Grace period duration must be greater than 0")

            if period_type not in ["MONTHLY", "QUARTERLY", "SEMI-ANNUALLY", "ANNUALLY"]:
                raise ValueError("Invalid period type")

            if grace_period_type not in ["NONE", "PARTIAL", "TOTAL"]:
                raise ValueError("Invalid grace period type")

        except (ValueError, TypeError) as e:
            raise ValueError("Invalid input data") from e

        return LoanParameters(
            bank_entity=bank_entity,
            total_years=total_years,
            vehicle_price=vehicle_price,
            vehicle_type=vehicle_type,
            down_payment=down_payment,
            financed_amount=financed_amount,
            tea_percentage=tea_percentage,
            balloon_payment=balloon_payment,
            grace_period_type=grace_period_type,
            grace_period_in_months=grace_period_in_months,
            vehicle_id=vehicle_id,
            user_id=user_id,
            period_type=period_type,
        )


class LoanFinancialIndicatorsService:
    @staticmethod
    def create(
            tcea_percentage: float,
            van: float,
            tir: float,
            loan_parameters_id: int,
    ) -> LoanFinancialIndicators:
        """ Create a new LoanFinancialIndicators instance. """

        try:
            tcea_percentage = float(tcea_percentage)
            if tcea_percentage < 0 or tcea_percentage > 1:
                raise ValueError("TEA percentage must be between 0 and 1")

            van = float(van)
            if van < 0:
                raise ValueError("VAN must be greater than 0")

            tir = float(tir)
            if tir < 0:
                raise ValueError("TIR must be greater than 0")

        except (ValueError, TypeError) as e:
            raise ValueError("Invalid input data") from e

        return LoanFinancialIndicators(
            tcea_percentage=tcea_percentage,
            van=van,
            tir=tir,
            loan_parameters_id=loan_parameters_id,
        )


class PaymentPeriodService:
    @staticmethod
    def create(
            period_number: int,
            date: str,
            balance_start: float,
            balance_end: float,
            interest: float,
            amortization: float,
            mortgage: float,
            vehicular_insurance: float,
            total_payment: float,
            grace_period_type: str,
    ) -> PaymentPeriod:
        """ Create a new PaymentPeriod instance. """

        try:
            period_number = int(period_number)
            if period_number < 0:
                raise ValueError("Period number must be greater than 0")

            balance_start = float(balance_start)
            if balance_start < 0:
                raise ValueError("Balance start must be greater than 0")

            balance_end = float(balance_end)
            if balance_end < 0:
                raise ValueError("Balance end must be greater than 0")

            interest = float(interest)
            if interest < 0:
                raise ValueError("Interest must be greater than 0")

            amortization = float(amortization)
            if amortization < 0:
                raise ValueError("Amortization must be greater than 0")

            mortgage = float(mortgage)
            if mortgage < 0:
                raise ValueError("Mortgage must be greater than 0")

            vehicular_insurance = float(vehicular_insurance)
            if vehicular_insurance < 0:
                raise ValueError("Vehicular insurance must be greater than 0")

            total_payment = float(total_payment)
            if total_payment < 0:
                raise ValueError("Total payment must be greater than 0")

            if grace_period_type not in ["NONE", "PARTIAL", "TOTAL"]:
                raise ValueError("Invalid grace period type")

            date = datetime.strptime(date, "%Y-%m-%d")
        except (ValueError, TypeError) as e:
            raise ValueError("Invalid input data") from e

        return PaymentPeriod(
            period_number=period_number,
            date=str(date),
            balance_start=balance_start,
            balance_end=balance_end,
            interest=interest,
            amortization=amortization,
            mortgage=mortgage,
            vehicular_insurance=vehicular_insurance,
            total_payment=total_payment,
            grace_period_type=grace_period_type,
        )


class PaymentScheduleService:
    @staticmethod
    def create(
            payment_periods: list[PaymentPeriod],
            loan_parameters_id: int,
    ) -> PaymentSchedule:
        """ Create a new PaymentSchedule instance. """

        total_interest: float = 0.0
        total_amortization: float = 0.0
        total_mortgage_protection_insurance: float = 0.0
        total_vehicular_insurance: float = 0.0
        total_payment: float = 0.0

        for period in payment_periods:
            total_interest += period.interest
            total_amortization += period.amortization
            total_mortgage_protection_insurance += period.mortgage
            total_vehicular_insurance += period.vehicular_insurance
            total_payment += period.total_payment

        payment_schedule = PaymentSchedule(
            total_interest=total_interest,
            total_amortization=total_amortization,
            total_mortgage_protection_insurance=total_mortgage_protection_insurance,
            total_vehicular_insurance=total_vehicular_insurance,
            total_payment=total_payment,
            loan_parameters_id=loan_parameters_id,
        )

        for period in payment_periods:
            period.payment_schedule_id = payment_schedule.payment_schedule_id

        payment_schedule.payment_periods = payment_periods

        return payment_schedule