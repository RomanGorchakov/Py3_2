#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sqlite3
import typing as t
from pathlib import Path
import unittest
import calc


def display_plane(staff: t.List[t.Dict[str, t.Any]]) -> None:
    if staff:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 12
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^12} |'.format(
                "No",
                "Destination",
                "Race number",
                "Plane type"
            )
        )
        print(line)
 
        for idx, planes in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>12} |'.format(
                    idx,
                    planes.get('race', ''),
                    planes.get('number', ''),
                    planes.get('type', 0)
                )
            )
            print(line)

    else:
        print("The flight list is empty.")


def create_db(database_path: Path) -> None:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cities (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            race_name INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            race_name TEXT NOT NULL,
            number_name INTEGER NOT NULL,
            type_name INTEGER NOT NULL,
            FOREIGN KEY(race_name) REFERENCES cities(race_name)
        )
        """
    )

    conn.close()


def add_plane(
    database_path: Path,
    race: str,
    number: int,
    type: int
) -> None:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT race_id FROM cities WHERE race_name = ?
        """,
        (race,)
    )
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            """
            INSERT INTO cities (race_name) VALUES (?)
            """,
            (race,)
        )
        race_id = cursor.lastrowid

    else:
        race_id = row[0]

    cursor.execute(
        """
        INSERT INTO races (race_name, number_name, type_name)
        VALUES (?, ?, ?)
        """,
        (race, number, type)
    )

    conn.commit()
    conn.close()


def select_allplanes(database_path: Path) -> t.List[t.Dict[str, t.Any]]:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT races.race_name, races.number_name, races.type_name
        FROM races
        INNER JOIN cities ON cities.race_id = races.race_id
        """
    )
    rows = cursor.fetchall()

    conn.close()
    return [
        {
            "race": row[0],
            "number": row[1],
            "type": row[2],
        }
            for row in rows
    ]


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--db",
        action="store",
        required=False,
        default=str(Path.home() / "workers.db"),
        help="The database file name"
    )

    parser = argparse.ArgumentParser("workers")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new race"
    )
    add.add_argument(
        "-r",
        "--race",
        action="store",
        required=True,
        help="The city where plane will go"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        type=int,
        required=True,
        help="The number of race"
    )
    add.add_argument(
        "-t",
        "--type",
        action="store",
        type=int,
        required=True,
        help="The type of plane"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all races"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the races"
    )
    select.add_argument(
        "-P",
        "--period",
        action="store",
        type=int,
        required=True,
        help="The required period"
    )

    args = parser.parse_args(command_line)

    db_path = Path(args.db)
    create_db(db_path)

    if args.command == "add":
        add_plane(db_path, args.race, args.number, args.type)

    elif args.command == "display":
        display_plane(select_allplanes(db_path))

class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        self.db_path = Path('test_planes.db')
        create_db(self.db_path)

    def tearDown(self):
        if self.db_path.exists():
            self.db_path.unlink()

    def test_create_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cities'")
        cities_table = cursor.fetchone()
        self.assertIsNotNone(cities_table, "Таблица 'Города' не создана")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='races'")
        races_table = cursor.fetchone()
        self.assertIsNotNone(races_table, "Таблица 'Рейсы' не создана")

        conn.close()

    def test_add_plane(self):
        add_plane(self.db_path, "Novoalexandrovsk", 3234, 62)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT race_name, number_name, type_name FROM races WHERE race_name = 'Novoalexandrovsk'")
        race = cursor.fetchone()

        self.assertIsNotNone(race, "Рейс не был добавлен")
        self.assertEqual(race[0], "Novoalexandrovsk", "Некорректное название рейса")
        self.assertEqual(race[1], 3234, "Некорректный номер рейса")
        self.assertEqual(race[2], 62, "Некорректный тип самолета")

        conn.close()

    def test_select_allplanes(self):
        add_plane(self.db_path, "Novoalexandrovsk", 3234, 62)
        add_plane(self.db_path, "Stavropol", 9120, 82)

        planes = select_allplanes(self.db_path)
        self.assertEqual(len(planes), 2, "Некорректное количество рейсов")
        
        first_plane = planes[0]
        self.assertEqual(first_plane["race"], "Novoalexandrovsk", "Некорректное название рейса")
        self.assertEqual(first_plane["number"], 3234, "Некорректный номер рейса")
        self.assertEqual(first_plane["type"], 62, "Некорректный тип самолета")

        second_plane = planes[1]
        self.assertEqual(second_plane["race"], "Stavropol", "Некорректное название рейса")
        self.assertEqual(second_plane["number"], 9120, "Некорректный номер рейса")
        self.assertEqual(second_plane["type"], 82, "Некорректный тип самолета")


if __name__ == "__main__":
    unittest.main()
    main()