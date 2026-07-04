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
        # Mortgage protection is charged on the financed amount, not the declining
        # balance, so it stays constant across every period — including the last one.
        last_mortgage_protection = 16.45875

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

        last_amortization_payment = 377.250327874237

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
        # Reflects the constant mortgage protection amount (see
        # test_last_mortgage_protection_is_correct) plus the balloon fee.
        last_total_payment = 10647.937214369362

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

    def test_mortgage_and_total_are_constant_across_regular_periods(self):
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

        regular_periods = schedule[:-1]  # excludes the last period, which adds the balloon fee

        mortgages = {round(p["mortgage"], 8) for p in regular_periods}
        totals = {round(p["total"], 6) for p in regular_periods}

        assert len(mortgages) == 1
        assert len(totals) == 1

    def test_grace_periods_are_part_of_the_total_term_not_extra(self):
        algorithm = FrenchMethodAlgorithm(
            vehicle_cost=28500.00,
            vehicle_type="MEDIUM_RISK",
            down_payment_percentage=0.25,
            balloon_payment_percentage=0.5,
            tea=0.10,
            initial_payment_date="2025-07-15",
            total_number_of_years=3,
            grace_period_type="PARTIAL",
            grace_period_in_months=1,
        )
        algorithm.perform()

        assert len(algorithm.payment_periods) == algorithm.number_of_periods