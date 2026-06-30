from analytics.domain.entities import LoanParameters, PaymentSchedule, PaymentPeriod, LoanFinancialIndicators
from analytics.infrastructure.models import LoanParametersModel, PaymentScheduleModel, PaymentPeriodModel, \
    LoanFinancialIndicatorsModel


class LoanParametersRepository:
    @staticmethod
    def save(loan_parameters: LoanParameters) -> LoanParameters:
        """ Persists loan parameters to the database. """

        model = LoanParametersModel.create(
            bank_entity=loan_parameters.bank_entity,
            total_years=loan_parameters.total_years,
            vehicle_price=loan_parameters.vehicle_price,
            vehicle_type=loan_parameters.vehicle_type,
            down_payment=loan_parameters.down_payment,
            financed_amount=loan_parameters.financed_amount,
            period_type=loan_parameters.period_type,
            tea_percentage=loan_parameters.tea_percentage,
            balloon_payment=loan_parameters.balloon_payment,
            grace_period_type=loan_parameters.grace_period_type,
            grace_period_in_months=loan_parameters.grace_period_in_months,
            vehicle_id=loan_parameters.vehicle_id,
            user_id=loan_parameters.user_id,
        )

        loan_parameters.loan_parameters_id = model.loan_parameters_id
        return loan_parameters

    @staticmethod
    def find_all_by_user_id(user_id: int) -> list[LoanParameters]:
        """ Finds all loan parameters for a specific user. """

        models = LoanParametersModel.filter(LoanParametersModel.user_id == user_id)
        entities: list[LoanParameters] = []

        for model in models:
            entity = LoanParameters(
                loan_parameters_id=model.loan_parameters_id,
                bank_entity=model.bank_entity,
                total_years=model.total_years,
                vehicle_price=model.vehicle_price,
                vehicle_type=model.vehicle_type,
                down_payment=model.down_payment,
                financed_amount=model.financed_amount,
                tea_percentage=model.tea_percentage,
                balloon_payment=model.balloon_payment,
                grace_period_type=model.grace_period_type,
                grace_period_in_months=model.grace_period_in_months,
                period_type=model.period_type,
                vehicle_id=model.vehicle_id,
                user_id=model.user_id,
            )
            entities.append(entity)

        return entities


class PaymentPeriodRepository:
    @staticmethod
    def save(payment_period: PaymentPeriod) -> PaymentPeriod:
        """ Persists payment periods to the database. """

        model = PaymentPeriodModel.create(
            period_number=payment_period.period_number,
            balance_start=payment_period.balance_start,
            balance_end=payment_period.balance_end,
            interest=payment_period.interest,
            amortization=payment_period.amortization,
            mortgage=payment_period.mortgage,
            vehicular_insurance=payment_period.vehicular_insurance,
            balloon_fee=payment_period.balloon_fee,
            total_payment=payment_period.total_payment,
            grace_period_type=payment_period.grace_period_type,
            net_flow=payment_period.net_flow,
            payment_date=payment_period.payment_date,
            payment_schedule_id=payment_period.payment_schedule_id,
        )

        payment_period.payment_period_id = model.payment_period_id
        return payment_period


class PaymentScheduleRepository:
    @staticmethod
    def save(payment_schedule: PaymentSchedule) -> PaymentSchedule:
        """ Persists payment schedule to the database. """

        model = PaymentScheduleModel.create(
            total_interest=payment_schedule.total_interest,
            total_amortization=payment_schedule.total_amortization,
            total_mortgage_protection_insurance=payment_schedule.total_mortgage_protection_insurance,
            total_vehicular_insurance=payment_schedule.total_vehicular_insurance,
            total_payment=payment_schedule.total_payment,
            loan_parameters_id=payment_schedule.loan_parameters_id,
        )

        payment_schedule.payment_schedule_id = model.payment_schedule_id
        return payment_schedule

    @staticmethod
    def find_by_loan_parameters_id(loan_parameters_id: int) -> PaymentSchedule:
        """ Finds the payment schedule for a specific set of parameters. """

        payment_schedule_model = PaymentScheduleModel.get_or_none(
            PaymentScheduleModel.loan_parameters_id == loan_parameters_id
        )
        if payment_schedule_model is None:
            return None

        payment_schedule_entity = PaymentSchedule(
            payment_schedule_id=payment_schedule_model.payment_schedule_id,
            total_interest=payment_schedule_model.total_interest,
            total_amortization=payment_schedule_model.total_amortization,
            total_mortgage_protection_insurance=payment_schedule_model.total_mortgage_protection_insurance,
            total_vehicular_insurance=payment_schedule_model.total_vehicular_insurance,
            total_payment=payment_schedule_model.total_payment,
            loan_parameters_id=payment_schedule_model.loan_parameters_id,
        )

        payment_periods = PaymentPeriodModel.filter(
            PaymentPeriodModel.payment_schedule_id == payment_schedule_model.payment_schedule_id
        )

        for period in payment_periods:
            payment_period_entity = PaymentPeriod(
                payment_period_id=period.payment_period_id,
                date=period.payment_date,
                period_number=period.period_number,
                balance_start=period.balance_start,
                balance_end=period.balance_end,
                interest=period.interest,
                amortization=period.amortization,
                mortgage=period.mortgage,
                vehicular_insurance=period.vehicular_insurance,
                balloon_fee=period.balloon_fee,
                total_payment=period.total_payment,
                net_flow=period.net_flow,
                grace_period_type=period.grace_period_type,
                payment_schedule_id=payment_schedule_model.payment_schedule_id,
            )

            payment_schedule_entity.add_payment_period(payment_period_entity)

        return payment_schedule_entity


class LoanFinancialIndicatorsRepository:
    @staticmethod
    def save(loan_financial_indicators: LoanFinancialIndicators) -> LoanFinancialIndicators:
        """ Persists loan financial indicators to the database. """

        model = LoanFinancialIndicatorsModel.create(
            tcea_percentage=loan_financial_indicators.tcea_percentage,
            van=loan_financial_indicators.van,
            tir=loan_financial_indicators.tir,
            loan_parameters_id=loan_financial_indicators.loan_parameters_id,
        )

        loan_financial_indicators.loan_simulation_id = model.loan_simulation_id
        return loan_financial_indicators

    @staticmethod
    def find_by_loan_parameters_id(loan_parameters_id: int) -> LoanFinancialIndicators:
        """ Finds loan financial indicators for a specific loan parameters. """

        model = LoanFinancialIndicatorsModel.get_or_none(
            LoanFinancialIndicatorsModel.loan_parameters_id == loan_parameters_id
        )
        if model is None:
            return None

        return LoanFinancialIndicators(
            loan_simulation_id=model.loan_simulation_id,
            tcea_percentage=model.tcea_percentage,
            van=model.van,
            tir=model.tir,
            loan_parameters_id=model.loan_parameters_id,
        )
