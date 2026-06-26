import pytest

from analytics.domain.algorithms import FrenchMethodAlgorithm


def build_schedule(**kwargs):
    algorithm = FrenchMethodAlgorithm(**kwargs)
    algorithm.perform()
    return algorithm.payment_periods


class TestAnalyticsDomainAlgorithms:

    def test_constant_installment_is_correct_according_to_example(self):
        constant_installment = 484.76596436935637

        algorithm = FrenchMethodAlgorithm(
            vehicle_cost=28500.00,
            vehicle_type="MEDIUM_RISK",
            down_payment_percentage=0.25,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="NONE",
            grace_period_in_months=6
        )

        assert algorithm.constant_installment == pytest.approx(constant_installment)

        schedule = build_schedule(
            vehicle_cost=algorithm.vehicle_cost,
            vehicle_type=algorithm.vehicle_type,
            down_payment_percentage=algorithm.down_payment_percentage,
            balloon_payment_percentage=algorithm.balloon_payment_percentage,
            tea=algorithm.tea,
            initial_payment_date=algorithm.initial_payment_date.strftime("%Y-%m-%d"),
            total_number_of_years=algorithm.total_number_of_years,
            grace_period_type=algorithm.grace_period_type,
            grace_period_in_months=algorithm.grace_period_in_months,
        )

        t0 = schedule[0]
        t1 = schedule[1]

        assert abs(
            (t0["interest"] + t0["amortization"]) -
            (t1["interest"] + t1["amortization"])
        ) < 1e-6

    def test_constant_vehicular_insurance_payment_is_correct(self):

        constant_vehicular_insurance = 171.7125

        schedule = build_schedule(
            vehicle_cost=28500.00,
            vehicle_type="PICK_UP",
            down_payment_percentage=0.25,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="NONE"
        )

        assert schedule[0]["vehicular"] == pytest.approx(constant_vehicular_insurance)

    def test_initial_mortgage_protection_is_correct(self):

        initial_mortgage_protection = 16.45875

        schedule = build_schedule(
            vehicle_cost=28500.00,
            vehicle_type="PICK_UP",
            down_payment_percentage=0.25,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="NONE"
        )

        assert schedule[0]["mortgage"] == pytest.approx(initial_mortgage_protection)

    def test_last_mortgage_protection_is_correct(self):

        last_mortgage_protection = 7.971232752463162

        schedule = build_schedule(
            vehicle_cost=28500.00,
            vehicle_type="PICK_UP",
            down_payment_percentage=0.25,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="NONE"
        )

        assert schedule[-1]["mortgage"] == pytest.approx(last_mortgage_protection)

    def test_first_amortization_payment_is_correct(self):

        first_amortization_payment = 262.77106883487136

        schedule = build_schedule(
            vehicle_cost=28500.00,
            vehicle_type="PICK_UP",
            down_payment_percentage=0.25,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="NONE"
        )

        assert schedule[0]["amortization"] == pytest.approx(first_amortization_payment)

    def test_last_amortization_payment_is_correct(self):

        last_amortization_payment = 10352.250327874237

        schedule = build_schedule(
            vehicle_cost=28500.00,
            vehicle_type="PICK_UP",
            down_payment_percentage=0.25,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="NONE"
        )

        assert schedule[-1]["amortization"] == pytest.approx(last_amortization_payment)

    def test_first_total_payment_is_correct(self):

        first_total_payment = 672.9372143693564

        schedule = build_schedule(
            vehicle_cost=28500.00,
            vehicle_type="PICK_UP",
            down_payment_percentage=0.25,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="NONE"
        )

        assert schedule[0]["total"] == pytest.approx(first_total_payment)

    def test_last_total_payment_is_correct(self):

        last_total_payment = 10639.44969712182

        schedule = build_schedule(
            vehicle_cost=28500.00,
            vehicle_type="PICK_UP",
            down_payment_percentage=0.25,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="NONE"
        )

        assert schedule[-1]["total"] == pytest.approx(last_total_payment)