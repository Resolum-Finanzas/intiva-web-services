from typing import Optional


class LoanParameters:
    """
    LoanParameters is a class that represents the parameters of a loan. It contains the following attributes:

    Attributes:
        bank_entity (str): The name of the bank entity that is providing the loan.
        total_years (int): The total number of years for the loan.
        vehicle_price (float): The price of the vehicle being financed.
        vehicle_type (str): The type of vehicle being financed.
        down_payment (float): The percentage of the vehicle price that is being paid as a down payment.
        financed_amount (float): The amount of the loan that is being financed.
        tea_percentage (float): The annual effective interest rate (TEA) percentage for the loan.
        balloon_payment (float): The percentage of the financed amount that is being paid as a balloon payment.
        grace_period_type (str): The type of grace period for the loan (e.g., "NONE", "PARTIAL", "TOTAL").
        grace_period_in_months (int): The number of months for the grace period.
        vehicle_id (int): The ID of the vehicle being financed.
        user_id (int): The ID of the user that is applying for the loan.
        loan_parameters_id (Optional[int]): An optional ID for the loan parameters.
        period_type (str): The type of payment period for the loan (e.g., "MONTHLY", "QUARTERLY", "ANNUAL").
    """

    def __init__(
            self,
            bank_entity: str,
            total_years: int,
            vehicle_price: float,
            vehicle_type: str,
            down_payment: float,
            financed_amount: float,
            tea_percentage: float,
            balloon_payment: float,
            grace_period_type: str, # NONE, PARTIAL, TOTAL
            vehicle_id: int,
            user_id: int,
            loan_parameters_id: Optional[int] = None,
            grace_period_in_months: int = 1,
            period_type: str = "MONTHLY",
    ):
        self.loan_parameters_id = loan_parameters_id
        self.bank_entity = bank_entity
        self.total_years = total_years
        self.vehicle_price = vehicle_price
        self.vehicle_type = vehicle_type
        self.down_payment = down_payment
        self.financed_amount = financed_amount
        self.period_type = period_type
        self.tea_percentage = tea_percentage
        self.balloon_payment = balloon_payment
        self.grace_period_type = grace_period_type
        self.grace_period_in_months = grace_period_in_months
        self.vehicle_id = vehicle_id
        self.user_id = user_id


class LoanFinancialIndicators:
    """
    LoanFinancialIndicators is a class that represents the financial indicators of a loan. It contains the following attributes:

    Attributes:
        tcea_percentage (float): The annual effective cost rate (TCEA) percentage for the loan.
        van (float): The net present value (VAN) of the loan.
        tir (float): The internal rate of return (TIR) of the loan.
        loan_parameters_id (int): The ID of the loan parameters associated with the financial indicators.
        payment_schedule_id (int): The ID of the payment schedule that is associated with the financial indicators.
        user_id (int): The ID of the user that is applying for the loan.
        loan_simulation_id (Optional[int]): An optional ID for the loan simulation associated with the financial indicators.
    """

    def __init__(
            self,
            tcea_percentage: float,
            van: float,
            tir: float,
            loan_parameters_id: int,
            payment_schedule_id: int,
            user_id: int,
            loan_simulation_id: Optional[int] = None
    ):
        self.loan_simulation_id = loan_simulation_id
        self.tcea_percentage = tcea_percentage
        self.van = van
        self.tir = tir
        self.loan_parameters_id = loan_parameters_id
        self.payment_schedule_id = payment_schedule_id
        self.user_id = user_id


class PaymentPeriod:
    """
    Represents a payment period in the amortization schedule of a loan.
    It contains details about the payment for that period, including the interest amount, amortization amount, insurance amounts, total payment, and the final balance at the end of the period.
    It also indicates whether the period is a balloon payment or a grace period.

    Attributes:
        period_number (int): The number of the payment period.
        balance_start (float): The balance at the start of the payment period.
        interest (float): The amount of interest paid during the payment period.
        amortization (float): The amount of principal paid during the payment period.
        mortgage (float): The amount of mortgage protection insurance paid during the payment period.
        vehicular_insurance (float): The amount of vehicular insurance paid during the payment period.
        total_payment (float): The total amount paid during the payment period, including interest, amortization, and insurance.
        balance_end (float): The balance at the end of the payment period.
        grace_period_type (str): The type of grace period for the payment period (e.g., "NONE", "PARTIAL", "TOTAL").
        payment_date (str): The date of the payment for the period.
        payment_schedule_id (Optional[int]): An optional ID linking to a specific payment schedule.
    """

    def __init__(
            self,
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
            payment_period_id: Optional[int] = None
    ):
        self.period_number = period_number
        self.balance_start = balance_start
        self.interest = interest
        self.amortization = amortization
        self.mortgage= mortgage
        self.vehicular_insurance = vehicular_insurance
        self.total_payment = total_payment
        self.balance_end = balance_end
        self.grace_period_type = grace_period_type
        self.payment_date = date
        self.payment_schedule_id = payment_period_id


class PaymentSchedule:
    """
    Represents the payment schedule for a loan, including total interest, amortization, insurance, and payments.

    Attributes:
        total_interest (float): The total interest paid on the loan.
        total_amortization (float): The total principal paid on the loan.
        total_mortgage_protection_insurance (float): The total amount of mortgage protection insurance paid on the loan.
        total_vehicular_insurance (float): The total amount of vehicular insurance paid on the loan.
        total_payment (float): The total amount paid on the loan, including interest, amortization, and insurance.
        payment_periods (list[PaymentPeriod]): A list of payment periods in the payment schedule.
    """

    def __init__(
            self,
            total_interest: float,
            total_amortization: float,
            total_mortgage_protection_insurance: float,
            total_vehicular_insurance: float,
            total_payment: float,
            payment_schedule_id: Optional[int] = None
    ):
        self.total_interest = total_interest
        self.total_amortization = total_amortization
        self.total_mortgage_protection_insurance = total_mortgage_protection_insurance
        self.total_vehicular_insurance = total_vehicular_insurance
        self.total_payment = total_payment
        self.payment_schedule_id = payment_schedule_id
        self.payment_periods = []

    def add_payment_period(self, period: PaymentPeriod):
        """
        Adds a payment period to the payment schedule.

        Args:
             period (PaymentPeriod): The payment period to be added.
        """

        self.payment_periods.append(period)