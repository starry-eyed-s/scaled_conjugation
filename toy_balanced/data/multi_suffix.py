## Script for generating training data with multiple suffix-variant conditions ##

import csv
import json

# --- Load classes: {class: {sid: stem}} ---
with open("toy_stems_with_id.json", "r", encoding="utf-8") as f:
    classes = json.load(f)

# --- FIXED suffix → p-ID mapping ---
ENDING_TO_P_FIXED = {
    "a":  "p0",
    "ta": "p1",
    "e":  "p2",
    "te": "p3",
    "i":  "p4",
    "ti": "p5",
    "o":  "p6",
    "to": "p7",
    "u":  "p8",
    "tu": "p9"
}


ENDINGS_POOL = ["a", "ta", "e", "te", "i", "ti", "o", "to", "u", "tu"]

VOWELS = {"a", "e", "i", "o", "u"}

def starts_with_vowel(x: str) -> bool:
    return x[0] in VOWELS

def starts_with_consonant(x: str) -> bool:
    return not starts_with_vowel(x)

# --- Candidate generator (3 candidates) ---
def generate_srs(stem, ending, stem_class):
    # coda rule: s -> t for s-class stems under consonant-initial suffix
    if stem_class.startswith("s") and starts_with_consonant(ending):
        stem_mod = stem[:-1] + "t"
    else:
        stem_mod = stem

    canonical = stem_mod + ending

    alt1 = stem[:-1] + "l" + ending   # ID-lat
    alt2 = stem[:-1] + ending         # Max (deletion)

    return [canonical, alt1, alt2]

def write_tsv(endings, filename):
    # fixed suffix IDs 
    ending_to_p = {e: ENDING_TO_P_FIXED[e] for e in endings}

    # collect (sid, stem, stem_class)
    pairs = []
    for stem_class, items in classes.items():
        for sid, stem in items.items():
            pairs.append((sid, stem, stem_class))

    # ensure s0, s1, s2... order
    pairs.sort(key=lambda x: int(x[0][1:]))

    with open(filename, "w", newline="", encoding="utf-8") as tsvfile:
        writer = csv.writer(tsvfile, delimiter="\t")

        # --- header: stem IDs + suffix IDs ---
        sids = [sid for sid, _, _ in pairs]
        suffix_ids = [ending_to_p[e] for e in endings]
        writer.writerow(sids + suffix_ids)


        # --- constraint names ---
        writer.writerow(["", "", "", "*V-Obs-V", "Max",  "ID-lat"])

        for sid, stem, stem_class in pairs:
            for ending in endings:
                input_id = f"{stem}-{ending}$$${sid}${ending_to_p[ending]}"
                candidates = generate_srs(stem, ending, stem_class)

                # winner logic: irregularity under vowel-initial suffix
                if starts_with_vowel(ending):
                    
                    if stem_class == "t-irregular":
                        winner_idx = 1
                    elif stem_class == "s-irregular":
                        winner_idx = 2
                    else:
                        winner_idx = 0
                else:
                    winner_idx = 0

                for idx, cand in enumerate(candidates):
                    perc = 1.0 if idx == winner_idx else 0.0
                    vc, mx, id_l = 0, 0, 0

                    if starts_with_vowel(ending) and idx == 0:
                        vc = 1
                    if idx == 1:
                        id_l = 1
                    if idx == 2:
                        mx = 1

                    row_input = input_id if idx == 0 else ""
                    writer.writerow([row_input, cand, perc, vc, mx, id_l])

def main():
    for n in (2, 4, 6, 8, 10):
        endings = ENDINGS_POOL[:n]
        filename = f"{n}suffix.tsv"
        write_tsv(endings, filename)

if __name__ == "__main__":
    main()
