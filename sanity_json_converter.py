import json
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Never, TypedDict, overload


class Entry(TypedDict):
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


class NS:
    def __getattr__(self, name: str) -> str | None:
        raise AttributeError(
            f"{self.__class__.__name__!r} object has no attribute {name!r}."
        )

    if TYPE_CHECKING:

        def __setattr__(self, name, setter) -> None:
            raise AttributeError(
                f"{self.__class__.__name__!r} object has no attribute {name!r}."
            )


@overload
def deformat_score(score: str) -> int: ...


@overload
def deformat_score(score: Literal[None]) -> None: ...


def deformat_score(score: str | None) -> int | None:
    if score is None:
        return None

    def dummy() -> Never:
        raise ValueError("Invalid score: %s" % score)

    def convert(times: int) -> int:
        assert score is not None
        try:
            return int(float(score) * times)
        except ValueError:
            dummy()

    try:
        return int(score)
    except ValueError:
        pass

    # case insesitive
    score = score.lower()

    if score.endswith("k"):
        score = score.removesuffix("k")
        return convert(1_000)

    elif score.endswith("m"):
        score = score.removesuffix("m")
        return convert(1_000_000)

    elif score.endswith("b"):
        score = score.removesuffix("b")
        return convert(100_000_000)

    dummy()


def sanity_converter(jsonpath: Path):
    contents: list[dict[str, str | None]] = json.load(jsonpath.open(encoding="utf-8"))
    new_contents: list[dict[str, str | None]] = []

    # here we try to convert the strings
    # to as much narrowed types as possible.
    # None (null) means the answer was written
    # incorrectly (invalid entry)

    for entry in contents:
        new = NS()
        ns = NS()
        ns.__dict__ |= entry

        new.time = ns.time
        new.age = int(ns.age) if ns.age is not None else None

        if ns.besttank is not None:
            new.besttank = [
                s.replace("-", " ").replace("/", " ").strip().title()
                for s in ns.besttank.split(",")
            ]
        else:
            new.besttank = None

        new.teamtype = ns.teamtype.strip().title() if ns.teamtype is not None else None

        if ns.favmodes is not None:
            new.favmodes = [
                s.replace("-", " ").replace("/", " ").strip().title()
                for s in ns.favmodes.split(",")
            ]
        else:
            new.favmodes = None

        # these are always LiteralStrings
        new.growth = ns.growth
        new.ar = ns.ar

        if ns.liketank is not None:
            new.liketank = [
                s.replace("-", " ").replace("/", " ").strip().title()
                for s in ns.liketank.split(",")
            ]
        else:
            new.liketank = None

        if ns.hatetank is not None:
            new.hatetank = [
                s.replace("-", " ").replace("/", " ").strip().title()
                for s in ns.hatetank.split(",")
            ]
        else:
            new.hatetank = None

        new.highscore = deformat_score(ns.highscore)

        new.highscoretank = (
            ns.highscoretank.strip().title() if ns.highscoretank is not None else None
        )

        new_contents.append(new.__dict__)

    with jsonpath.with_stem(f"Sane {jsonpath.stem}").open("w") as sane_json:
        json.dump(obj=new_contents, fp=sane_json, indent=4)


sanity_converter(Path("arrasds.json"))
