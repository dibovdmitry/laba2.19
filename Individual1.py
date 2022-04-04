#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from pathlib import Path


def add_airplane(race, path, number, model):
    race.append(
        {
            "path": path,
            "number": number,
            "model": model
        }
    )

    return race


def display_airplanes(race):
    if race:

        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "№",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолёта"
            )
        )
        print(line)

        for idx, airplane in enumerate(race, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                    idx,
                    airplane.get('path', ''),
                    airplane.get('number', ''),
                    airplane.get('model', 0)
                )
            )
            print(line)

    else:
        print("Список работников пуст.")


def select_airplanes(race, sel):

    result = []
    for airplane in race:
        if airplane.get('path') <= sel:
            result.append(airplane)

    return result


def save_airplanes(file_name, way, save_home):
    if save_home:
        place = Path.home() / file_name
        with open(place, "w") as f:
            json.dump(way, f, ensure_ascii=False, indent=4)
    else:
        place = Path.cwd() / file_name
        with open(place, "w") as f:
            json.dump(way, f, ensure_ascii=False, indent=4)


def load_airplanes(file_name, save_home):
    if save_home:
        place = Path.home() / file_name
        with open(place, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    parser = argparse.ArgumentParser("airplanes")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new airplane"
    )
    add.add_argument(
        "-p",
        "--path",
        action="store",
        required=True,
        help="The airplane's path"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        help="The airplane's number"
    )
    add.add_argument(
        "-m",
        "--model",
        action="store",
        type=int,
        required=True,
        help="The airplane's model"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all airplanes"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the airplanes"
    )
    select.add_argument(
        "-r",
        "--result",
        action="store",
        type=int,
        required=True,
        help="The required result"
    )

    args = parser.parse_args(command_line)

    if Path(args.filename).exists():
        airplanes = load_airplanes(args.filename, args.home)
    else:
        airplanes = []

    if args.command == "add":
        airplanes = add_airplane(
            airplanes,
            args.path,
            args.number,
            args.model
        )
        save_airplanes(args.filename, airplanes, args.home)

    elif args.command == "display":
        display_airplanes(airplanes)
    elif args.command == "select":
        selected = select_airplanes(airplanes, args.result)
        display_airplanes(selected)

    selected = select_airplanes(airplanes)
    display_airplanes(selected)


if __name__ == "__main__":
    main()
