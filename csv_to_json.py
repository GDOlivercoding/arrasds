import csv
import json
from pathlib import Path


def convert_csv_to_json(csvpath: Path, *, map: dict[str, str] | None = None):
    with csvpath.open("r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        d: list[dict[str, str]] = []
        if map is None:
            with csvpath.with_suffix(".json").open("w") as js:
                js.write(json.dumps(list(reader), indent=4))
                return 
        
        for entry in reader:
            d.append({map[k]: v for k, v in entry.items()})

        with csvpath.with_suffix(".json").open("w") as js:
            js.write(json.dumps(d, indent=4))

text_mapping = {
    "Časová značka": "time",
    "How old are you? (This is completely anonymized)": "age",
    "What do you think is the best tank in normal arras.io? (There are different choices so it will be easier to parse later on, these are the most popular picks)": "besttank",
    "Whats your favorite team type? (Other if it is not mentioned, if it falls under one of these categories, please pick)": "teamtype",
    "Whats your favorite gamemode? this can be absolutely anything, ranging from simple 2tdm, to arms race, growth, Capture the Flag, soccer, tetromino, half growth, dv1, dv2 & dv3, make sure it has existed at least once, you can pick multiple (seperate by commas)": "favmodes",
    "How do you feel about growth modes? (Any mode with Growth/Overgrowth)": "growth",
    "How do you feel about Arms Race modes?": "ar",
    "What tank do you like the most? (no arms race please)": "liketank",
    "What tank do you hate the most? (When facing them, no arms race)": "hatetank",
    "Whats your highscore in normal modes? (No arms race, minigames or growth)": "highscore",
    "Following the last question, what tank did you use?": "highscoretank"
}