from peewee import Model, AutoField, CharField, IntegerField, FloatField

from shared.infrastructure.database import db


class LoanParametersModel(Model):
    loan_parameters_id = AutoField()
    bank_entity = CharField()
    total_years = IntegerField()
    vehicle_price = FloatField()
    vehicle_type = CharField()
    down_payment = FloatField()
    financed_amount = FloatField()
    period_type = CharField(default="MONTHLY")
    tea_percentage = FloatField()
    balloon_payment = FloatField()
    grace_period_type = CharField(default="NONE")
    grace_period_in_months = IntegerField(default=0)
    vehicle_id = IntegerField()
    user_id = IntegerField()

    class Meta:
        database = db
        table_name = "loan_parameters"


class PaymentScheduleModel(Model):
    payment_schedule_id = AutoField()
    total_interest = FloatField()
    total_amortization = FloatField()
    total_mortgage_protection_insurance = FloatField()
    total_vehicular_insurance = FloatField()
    total_payment = FloatField()
    loan_parameters_id = IntegerField()

    class Meta:
        database = db
        table_name = "payment_schedules"


class PaymentPeriodModel(Model):
    payment_period_id = AutoField()
    period_number = IntegerField()
    balance_start = FloatField()
    balance_end = FloatField()
    interest = FloatField()
    amortization = FloatField()
    mortgage = FloatField()
    vehicular_insurance = FloatField()
    balloon_fee = FloatField()
    total_payment = FloatField()
    grace_period_type = CharField(default="NONE")
    net_flow = FloatField()
    payment_date = CharField()
    payment_schedule_id = IntegerField()

    class Meta:
        database = db
        table_name = "payment_periods"


class LoanFinancialIndicatorsModel(Model):
    loan_simulation_id = AutoField()
    tcea_percentage = FloatField()
    van = FloatField()
    tir = FloatField()
    loan_parameters_id = IntegerField()

    class Meta:
        database = db
        table_name = "loan_financial_indicators"
