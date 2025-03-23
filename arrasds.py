from collections.abc import Iterable, Iterator, Sequence
from typing import Any, Never, Self
import csv
from dataclasses import dataclass
from datetime import datetime
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
            raise AttributeError(f"{self.__class__.__name__!r} object has no attribute {name!r}.")

    def __repr__(self):
        return f"<Entry {" ".join([f"{k}={str(v)}" for k, v in vars(self).items()])}>"

def get_iter(contents: Sequence[Entry], attrname: str) -> list[Any]:
    """
    Return a flattened list containing all values   
    of the Entries in the contents, without 'None's
    return type is list[T] where T is the getter return type for attrname of Entry objects
    consider narrowing the typehinting upon assignment
    """
    if contents:
        if not hasattr(contents[0], attrname):
            raise AttributeError(f"{contents[0].__class__.__name__!r} object has no attribute {attrname!r}.")
    else:
        if attrname not in dir(Entry):
            raise AttributeError(f"{Entry.__name__!r} object has no attribute {attrname!r}.")
        return []
    
    return [
        item
        for entry in contents
        for listornot in (
            getattr(entry, attrname)
            if isinstance(getattr(entry, attrname), Iterable)
            else [getattr(entry, attrname)]
        )
        for item in (
            listornot 
            if isinstance(listornot, list) 
            else [listornot]
        )
        if item is not None
    ]

# im going to create some ds snippets in advance here


ds_file = Path("sane_arrasds.json")

contents: list[Entry] = [Entry(**e) for e in json.load(ds_file.open())]

def count_per_age():
    ages: list[int] = get_iter(contents, 'age')

    ages_x = [*range(min(ages), max(ages)+1)]

    counts = [ages.count(i) for i in ages_x]

    plt.plot(ages_x, counts, label='Player Count')
    plt.yticks([*range(min(counts), max(counts)+1)])
    plt.ylabel('Count')
    plt.xlabel('Age')
    plt.title('Amount of people that play to age')

def favorite_tanks():
    # This whole function is a little weird and cursed,
    # first, let's recognize the way nested for loops work
    # in list comprehensions.
    tanks: list[str] = get_iter(contents, 'liketank')
    # We sort the dict, by value and return keys

    d: dict[str, int] = {}

    for i in tanks:
        item = d.get(i, 0) + 1
        d[i] = item

    sorted_tanks = sorted(d, key=d.__getitem__)
     
    sorted_counts = sorted(d.values())
    counts_x = range(len(sorted_tanks))

    #print(len(counts_x), len(sorted_tanks), len(sorted_counts))
    assert len(counts_x) == len(sorted_tanks)
    for count, tank in zip(sorted_counts, sorted_tanks):
        print(tank)

    plt.xticks(ticks=counts_x, labels=sorted_tanks)
    plt.yticks([*range(min(counts_x), max(counts_x)+1)])
    plt.bar(counts_x, sorted_counts)
    plt.title("Favorite tanks")

def average_score():
    avg_scores: list[int] = get_iter(contents, 'highscore')
    avg_score = int(sum(avg_scores) / len(avg_scores))

    print(avg_score)

    dummy: tuple[int] = (1,)

    # doesnt work quite right
    plt.xticks(ticks=dummy, labels=("Average Score",))
    plt.yticks(dummy + (avg_score,))
    plt.bar(dummy, (avg_score,))
    plt.title("Average Score")

if __name__ == "__main__":
    from matplotlib import pyplot as plt

    # function call here
    favorite_tanks()

    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()