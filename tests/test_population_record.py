import pytest

from src.population_record import CountryPopulationRecord


@pytest.fixture
def valid_record_data():
    return {"country": "Ukraine", "year": 2020, "population": 44134693}


def test_create_country_population_record(valid_record_data):
    record = CountryPopulationRecord(**valid_record_data)

    assert record.country == "Ukraine"
    assert record.year == 2020
    assert record.population == 44134693


@pytest.mark.parametrize(
    "payload",
    [
        {"country": "", "year": 2020, "population": 1},
        {"country": "   ", "year": 2020, "population": 1},
        {"country": "Ukraine", "year": -1, "population": 1},
        {"country": "Ukraine", "year": 2020, "population": -1},
    ],
)
def test_create_country_population_record_invalid(payload):
    with pytest.raises(ValueError):
        CountryPopulationRecord(**payload)
