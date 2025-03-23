from collections.abc import Iterable, Sequence
from datetime import datetime
from typing import Any
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class Entry:
    time: str
    age: int | None
    besttank: list[str] | None
    teamtype: str | None
    favmodes: list[str] | None
    growth: str
    ar: str
    liketank: list[str] | None
    hatetank: list[str] | None
    highscore: int | None
    highscoretank: str | None

    class CustomNamespace:
        """
        A namespace for an entry.
        Just a simple namespace with a little bit of typing.
        """

        def __getattr__(self, name: str) -> str:
            raise AttributeError(
                f"{self.__class__.__name__!r} object has no attribute {name!r}."
            )

    def __repr__(self):
        return f"<Entry {' '.join([f'{k}={str(v)}' for k, v in vars(self).items()])}>"

    def time_to_datetime(self) -> datetime:
        dmy, _, hms = self.time.partition(" ")
        day, month, year = [int(s) for s in dmy.split(".")]
        hour, minute, second = [int(s) for s in hms.split(":")]
        return datetime(
            year=year, month=month, day=day, hour=hour, minute=minute, second=second
        )


def get_iter(contents: Sequence[Entry], attrname: str) -> list[Any]:
    """
    Return a flattened list containing all values
    of the Entries in the contents, without 'None's
    return type is list[T] where T is the getter return type for attrname of Entry objects
    consider narrowing the typehinting upon assignment
    """
    if contents:
        if not hasattr(contents[0], attrname):
            raise AttributeError(
                f"{contents[0].__class__.__name__!r} object has no attribute {attrname!r}."
            )
    else:
        if attrname not in dir(Entry):
            raise AttributeError(
                f"{Entry.__name__!r} object has no attribute {attrname!r}."
            )
        return []

    return [
        item
        for entry in contents
        for listornot in (
            getattr(entry, attrname)
            if isinstance(getattr(entry, attrname), Iterable)
            and not isinstance(getattr(entry, attrname), str)
            else [getattr(entry, attrname)]
        )
        for item in (listornot if isinstance(listornot, list) else [listornot])
        if item is not None
    ]


def sort_dict[K, V: Any](d: dict[K, V]) -> dict[K, V]:
    return {k: d[k] for k in sorted(d, key=d.__getitem__, reverse=True)}


ds_file = Path("sane_arrasds.json")

contents: list[Entry] = [Entry(**e) for e in json.load(ds_file.open())]


def invalid_fav_tanks():
    print(
        f"And there were {sum(1 for tank in [s.liketank for s in contents] if tank is None)} invalid picks."
    )
    print(f"Out of {len(contents)} submissions.")


def average_age():
    avg_ages = get_iter(contents, "age")
    avg_age = sum(avg_ages) / len(avg_ages)
    print(f"Average age of an arrasio player: {avg_age:.1f}")


def average_date_submitted_at():
    datetimes = [e.time_to_datetime() for e in contents]

    def most_datetime(key: str) -> dict[int, int]:
        d = {}
        for dt in datetimes:
            obj = getattr(dt, key)
            item = d.get(obj, 0) + 1
            d[obj] = item
        return d

    average_day = most_datetime("day")
    average_hour = most_datetime("hour")
    average_minute = most_datetime("minute")
    average_second = most_datetime("second")

    print(
        sort_dict(average_day),
        sort_dict(average_hour),
        sort_dict(average_minute),
        sort_dict(average_second),
        sep="\n",
    )


def most_hated_tank():
    print("Most hated tanks: ")

    tanks: list[str] = get_iter(contents, "hatetank")

    d: dict[str, int] = {}

    for tank in tanks:
        item = d.get(tank, 0) + 1
        d[tank] = item

    sorted_tanks = sort_dict(d)

    for tank, count in sorted_tanks.items():
        print(f"{tank}: {count}")
        # print(tank)


def favorite_modes():
    print("Favorite modes: ")

    modes: list[str] = get_iter(contents, "favmodes")

    d: dict[str, int] = {}

    for mode in modes:
        item = d.get(mode, 0) + 1
        d[mode] = item

    sorted_modes = sort_dict(d)

    for mode, count in sorted_modes.items():
        print(f"{mode}: {count}")
        # print(mode)


def favorite_mode_tag():
    print("Favorite tags: ")

    tags: list[str] = [
        tag.strip().title()
        for mode in get_iter(contents, "favmodes")
        for tag in mode.split(" ")
    ]

    d: dict[str, int] = {}

    for tag in tags:
        item = d.get(tag, 0) + 1
        d[tag] = item

    sorted_tags = sort_dict(d)

    for tag, count in sorted_tags.items():
        # print(f"{tag}: {count}")
        print(tag)


def youngest_submittor():
    ages = get_iter(contents, "age")
    print(f"Youngest Submittor: {min(ages)}")


def oldest_submittor():
    ages = get_iter(contents, "age")
    print(f"Oldest Submittor: {max(ages)}")


