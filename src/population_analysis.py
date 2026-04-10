"""Прості функції для аналізу популяції з txt-файлу."""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from src.population_record import CountryPopulationRecord


def parse_population_line(line: str) -> CountryPopulationRecord:
    """Розбирає один рядок формату: country, year, population."""
    parts = [part.strip() for part in line.split(",")]
    if len(parts) != 3:
        raise ValueError(
            "Each line must contain exactly three values: "
            "country, year, population."
        )

    country, year_raw, population_raw = parts
    country = country.lstrip("\ufeff")
    try:
        year = int(year_raw)
        population = int(population_raw)
    except ValueError as exc:
        raise ValueError("Year and population must be integers.") from exc

    return CountryPopulationRecord(
        country=country,
        year=year,
        population=population,
    )


def read_population_file(
    file_path: str | Path,
) -> list[CountryPopulationRecord]:
    """Читає txt-файл і повертає список валідних записів."""
    path = Path(file_path)
    if path.suffix.lower() != ".txt":
        raise ValueError("Input file must have .txt extension.")

    records: list[CountryPopulationRecord] = []
    for line_no, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        1,
    ):
        line = raw_line.strip()
        # Порожні рядки просто пропускаємо.
        if not line:
            continue
        try:
            records.append(parse_population_line(line))
        except ValueError as exc:
            raise ValueError(f"Invalid data at line {line_no}: {exc}") from exc

    return records


def calculate_population_changes(
    records: list[CountryPopulationRecord],
) -> dict[str, list[tuple[int, int, int | None]]]:
    """Рахує зміну населення по роках для кожної країни."""
    grouped: dict[str, list[CountryPopulationRecord]] = {}
    for record in records:
        if record.country not in grouped:
            grouped[record.country] = []
        grouped[record.country].append(record)

    changes: dict[str, list[tuple[int, int, int | None]]] = {}
    for country, country_records in grouped.items():
        sorted_records = sorted(country_records, key=lambda rec: rec.year)
        previous_population: int | None = None
        rows: list[tuple[int, int, int | None]] = []

        for item in sorted_records:
            # Для першого року беремо зміну як 0, щоб вивід був простішим.
            delta = 0
            if previous_population is not None:
                delta = item.population - previous_population
            rows.append((item.year, item.population, delta))
            previous_population = item.population

        changes[country] = rows

    return changes


def format_population_changes(
    changes: dict[str, list[tuple[int, int, int | None]]],
) -> str:
    """Форматує результат у простий текст для консолі."""
    lines: list[str] = []
    for country in sorted(changes):
        lines.append(f"{country}:")
        for year, population, delta in changes[country]:
            delta_text = f"{delta:+d}" if delta is not None else "+0"
            lines.append(
                f"  {year}: population={population}, change={delta_text}"
            )

    return "\n".join(lines)


def analyze_population_file(
    file_path: str | Path,
) -> dict[str, list[tuple[int, int, int | None]]]:
    """Запускає ланцюжок: читання, обчислення, повернення результату."""
    records = read_population_file(file_path)
    return calculate_population_changes(records)


def main() -> None:
    """Точка входу CLI для аналізу популяції."""
    parser = ArgumentParser(
        description=(
            "Read a .txt file with lines in format "
            "'country, year, population' "
            "and show population changes by years."
        )
    )
    parser.add_argument(
        "file_path",
        help="Path to input .txt file",
    )
    args = parser.parse_args()

    result = analyze_population_file(args.file_path)
    print(format_population_changes(result))
