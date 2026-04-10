from pathlib import Path

import pytest

from src.population_analysis import analyze_population_file
from src.population_analysis import calculate_population_changes
from src.population_analysis import format_population_changes
from src.population_analysis import parse_population_line
from src.population_analysis import read_population_file
from src.population_record import CountryPopulationRecord


@pytest.fixture
def sample_records() -> list[CountryPopulationRecord]:
    return [
        CountryPopulationRecord("Ukraine", 2020, 44134693),
        CountryPopulationRecord("Ukraine", 2021, 43792855),
        CountryPopulationRecord("Poland", 2020, 37846611),
        CountryPopulationRecord("Poland", 2021, 37797327),
    ]


@pytest.fixture
def sample_population_file(tmp_path: Path) -> Path:
    file_path = tmp_path / "population.txt"
    file_path.write_text(
        "\n".join(
            [
                "Ukraine, 2021, 43792855",
                "Ukraine, 2020, 44134693",
                "",
                "Poland, 2020, 37846611",
                "Poland, 2021, 37797327",
            ]
        ),
        encoding="utf-8",
    )
    return file_path


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "Ukraine, 2020, 44134693",
            CountryPopulationRecord("Ukraine", 2020, 44134693),
        ),
        (
            "\ufeffUkraine, 2020, 44134693",
            CountryPopulationRecord("Ukraine", 2020, 44134693),
        ),
        (
            "Poland,2021,37797327",
            CountryPopulationRecord("Poland", 2021, 37797327),
        ),
    ],
)
def test_parse_population_line_valid(line, expected):
    assert parse_population_line(line) == expected


@pytest.mark.parametrize(
    "bad_line",
    [
        "",
        "OnlyCountry",
        "Ukraine, text, 1",
        "Ukraine, 2020, text",
    ],
)
def test_parse_population_line_invalid(bad_line):
    with pytest.raises(ValueError):
        parse_population_line(bad_line)


def test_read_population_file(sample_population_file):
    result = read_population_file(sample_population_file)

    assert len(result) == 4
    assert result[0] == CountryPopulationRecord("Ukraine", 2021, 43792855)


@pytest.mark.parametrize(
    "file_name",
    ["population.csv", "population.json"],
)
def test_read_population_file_invalid_extension(
    tmp_path: Path,
    file_name: str,
):
    file_path = tmp_path / file_name
    file_path.write_text(
        "Ukraine, 2020, 44134693",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        read_population_file(file_path)


def test_calculate_population_changes(sample_records):
    changes = calculate_population_changes(sample_records)

    assert changes["Ukraine"] == [
        (2020, 44134693, 0),
        (2021, 43792855, -341838),
    ]
    assert changes["Poland"] == [
        (2020, 37846611, 0),
        (2021, 37797327, -49284),
    ]


def test_format_population_changes(sample_records):
    changes = calculate_population_changes(sample_records)

    output = format_population_changes(changes)

    assert "Poland:" in output
    assert "Ukraine:" in output
    assert "2020: population=44134693, change=+0" in output
    assert "2021: population=43792855, change=-341838" in output


def test_analyze_population_file(sample_population_file):
    changes = analyze_population_file(sample_population_file)

    assert set(changes.keys()) == {"Ukraine", "Poland"}
    assert changes["Poland"][1][2] == -49284
