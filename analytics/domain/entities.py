from datetime import datetime
from typing import Optional


class LoanParameters:
    """
    LoanParameters is a class that represents the parameters of a loan. It contains the following attributes:

    Attributes:
        bank_entity (str): The name of the bank entity that provides the loan.
        credit_term_in_months (int): The term of the loan in months.
        initial_payment_amount (float): The amount of the initial payment for the loan.
        credit_price (float): The price of the credit for the loan. It is the price of the vehicle.
        financed_amount (float): The amount of the loan that is financed.
        payment_frequency (str): The frequency of the payments for the loan. It can be "monthly", "biweekly", or "weekly".
        tea_percentage (float): The annual effective rate (TEA) percentage for the loan.
        balloon_payment_percentage (float): The percentage of the balloon payment for the loan. It is the percentage of the financed amount that will be paid at the end of the loan term.
        vehicular_insurance_enabled (bool): A boolean that indicates if the vehicular insurance is enabled for the loan.
        vehicular_insurance_amount (float): The amount of the vehicular insurance for the loan.
        mortgage_protection_insurance_enabled (bool): A boolean that indicates if the mortgage protection insurance is enabled for the loan.
        mortgage_protection_insurance_amount (float): The amount of the mortgage protection insurance for the loan.
        grace_period_enabled (bool): A boolean that indicates if the grace period is enabled for the loan.
        grace_period_type (str): The type of the grace period for the loan. It can be "total" or "partial".
        grace_period_in_months (int): The number of months of the grace period for the loan.
        vehicle_id (str): The ID of the vehicle that is being financed with the loan.
        user_id (str): The ID of the user that is taking the loan.
    """

    def __init__(
            self,
            bank_entity: str,
            credit_term_in_months: int,
            initial_payment_amount: float,
            credit_price: float,
            financed_amount: float,
            payment_frequency: str,
            tea_percentage: float,
            balloon_payment_percentage: float,
            vehicular_insurance_enabled: bool,
            vehicular_insurance_amount: float,
            mortgage_protection_insurance_enabled: bool,
            mortgage_protection_insurance_amount: float,
            grace_period_enabled: bool,
            grace_period_type: str,
            grace_period_in_months: int,
            vehicle_id: int,
            user_id: int,
            loan_parameters_id: Optional[int] = None
    ):
        self.loan_parameters_id = loan_parameters_id
        self.bank_entity = bank_entity
        self.credit_term_in_months = credit_term_in_months
        self.initial_payment_amount = initial_payment_amount
        self.credit_price = credit_price
        self.financed_amount = financed_amount
        self.payment_frequency = payment_frequency
        self.tea_percentage = tea_percentage
        self.balloon_payment_percentage = balloon_payment_percentage
        self.vehicular_insurance_enabled = vehicular_insurance_enabled
        self.vehicular_insurance_amount = vehicular_insurance_amount
        self.mortgage_protection_insurance_enabled = mortgage_protection_insurance_enabled
        self.mortgage_protection_insurance_amount = mortgage_protection_insurance_amount
        self.grace_period_enabled = grace_period_enabled
        self.grace_period_type = grace_period_type
        self.grace_period_in_months = grace_period_in_months
        self.vehicle_id = vehicle_id
        self.user_id = user_id


class LoanSimulation:
    """
    LoanSimulation is a class that represents the results of a loan simulation. It contains the following attributes:

    Attributes:
        tcea_percentage (float): The annual effective cost rate (TCEA) percentage for the loan simulation.
        ballon_payment_amount (float): The amount of the balloon payment for the loan simulation.
        van (float): The net present value (VAN) of the loan simulation.
        tir (float): The internal rate of return (TIR) of the loan simulation.
        grace_interest (float): The amount of interest that is paid during the grace period for the loan simulation.
        loan_parameters_id (str): The ID of the loan parameters that were used for the loan simulation.
        payment_schedule_id (str): The ID of the payment schedule that was generated for the loan simulation.
        user_id (str): The ID of the user that performed the loan simulation.
    """

    def __init__(
            self,
            tcea_percentage: float,
            ballon_payment_amount: float,
            van: float,
            tir: float,
            grace_interest: float,
            loan_parameters_id: int,
            payment_schedule_id: int,
            user_id: int,
            loan_simulation_id: Optional[int] = None
    ):
        self.loan_simulation_id = loan_simulation_id
        self.tcea_percentage = tcea_percentage
        self.ballon_payment_amount = ballon_payment_amount
        self.van = van
        self.tir = tir
        self.grace_interest = grace_interest
        self.loan_parameters_id = loan_parameters_id
        self.payment_schedule_id = payment_schedule_id
        self.user_id = user_id


class PaymentPeriod:
    """
    Represents a payment period in the amortization schedule of a loan.
    It contains details about the payment for that period, including the interest amount, amortization amount, insurance amounts, total payment, and the final balance at the end of the period.
    It also indicates whether the period is a balloon payment or a grace period.

    Attributes:
        period_number (int): The number of the payment period (e.g., 1 for the first period).
        current_balance (float): The outstanding balance at the beginning of the period.
        interest_amount (float): The amount of interest paid during the period.
        amortization_amount (float): The amount of principal paid during the period.
        mortgage_protection_insurance_amount (float): The amount paid for mortgage protection insurance during the period.
        vehicular_insurance_amount (float): The amount paid for vehicular insurance during the period.
        total_payment (float): The total payment made during the period, including interest, amortization, and insurance amounts.
        final_balance_at_end_of_period (float): The outstanding balance at the end of the period after making the payment.
        is_balloon (bool): Indicates whether this payment is a balloon payment.
        is_grace_period (bool): Indicates whether this period is a grace period where no payments are made.
        payment_date (datetime): The date on which the payment is made.
        payment_schedule_id (str): The ID of the payment schedule that this payment period belongs to.
    """

    def __init__(
            self,
            period_number: int,
            current_balance: float,
            interest_amount: float,
            amortization_amount: float,
            mortgage_protection_insurance_amount: float,
            vehicular_insurance_amount: float,
            total_payment: float,
            final_balance_at_end_of_period: float,
            is_balloon: bool,
            is_grace_period: bool,
            payment_date: datetime,
            payment_period_id: Optional[int] = None
    ):
        self.period_number = period_number
        self.current_balance = current_balance
        self.interest_amount = interest_amount
        self.amortization_amount = amortization_amount
        self.mortgage_protection_insurance_amount= mortgage_protection_insurance_amount
        self.vehicular_insurance_amount = vehicular_insurance_amount
        self.total_payment = total_payment
        self.final_balance_at_end_of_period = final_balance_at_end_of_period
        self.is_balloon = is_balloon
        self.is_grace_period = is_grace_period
        self.payment_date = payment_date
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
        total_grace_interest (float): The total amount of interest paid during the grace period.
        payment_periods (list[PaymentPeriod]): A list of payment periods in the payment schedule.
    """

    def __init__(
            self,
            total_interest: float,
            total_amortization: float,
            total_mortgage_protection_insurance: float,
            total_vehicular_insurance: float,
            total_payment: float,
            total_grace_interest: float,
            payment_schedule_id: Optional[int] = None
    ):
        self.total_interest = total_interest
        self.total_amortization = total_amortization
        self.total_mortgage_protection_insurance = total_mortgage_protection_insurance
        self.total_vehicular_insurance = total_vehicular_insurance
        self.total_payment = total_payment
        self.total_grace_interest = total_grace_interest
        self.payment_schedule_id = payment_schedule_id
        self.payment_periods = []

    def add_payment_period(self, period: PaymentPeriod):
        """
        Adds a payment period to the payment schedule.

        Args:
             period (PaymentPeriod): The payment period to be added.
        """

        self.payment_periods.append(period)