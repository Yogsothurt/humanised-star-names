import hashlib
import json
import re
import sys

CODE_RE = re.compile(r"^[A-Z]{2}-[A-Z]$", re.IGNORECASE)

ROOTS = [
    "Val", "Mor", "Kal", "Tel", "Tor", "Bel", "Sel", "Gal",
    "Nor", "Cor", "Lar", "Fen", "Zar", "Mar", "Ver", "Dor",
    "Ael", "Ryn", "Tha", "Vel", "Eld", "Ser", "Ith", "Rav",
    "Lum", "Kel", "Orr", "Dra", "Myr", "Fal", "Tal", "Vor"
]


ROOTS += [
    'Lav', 'Rom', 'Lak', 'Let', 'Ron', 'Leb', 'Les', 'Lag',
    'Rot', 'Roc', 'Ral', 'Nef', 'Raz', 'Ram', 'Rev', 'Rod',
    'Lea', 'Nyr', 'Aht', 'Lev', 'Dle', 'Res', 'Hti', 'Var',
    'Mul', 'Lek', 'Rro', 'Ard', 'Rym', 'Laf', 'Lat', 'Rov']

ROOTS += [
    "Dry", "Fly", "Syn", "Pry",
    "Thae", "Xan", "Khy", "Vyr",
    "Tyr", "Shae", "Phae", "Zhy"
]


MIDDLES = [
    "", "i", "", "",

    # Single vowels
    "a", "e", "", "o", "u", "y",

    # Traditional pairs
    "ae", "ai", "ao",
    "ea", "ei", "eo",
    "ia", "ie", "io",
    "oa", "oe", "oi",
    "ou",
    "ua", "ue", "ui", "uo",

    # Y combinations
    "ay", "ey", "iy", "oy", "uy",
    "ya", "ye", "yi", "yo", "yu",

    # More Elite-sounding
    "yae", "yea", "yia",
    "aey", "eya", "iya",
    "ayo", "eyo", "iyo",

    # Exotic combinations
    "au", "eu", "iu",
    "oae", "eou", "uae"
]

ENDINGS = [
    "a", "on", "ar", "ia", "ius", "ion", "or", "oria",
    "eron", "aris", "eth", "ara", "os", "ean", "ir",
    "ora", "arae", "iona", "oran", "eus", "ith"
]


ENDINGS += [
    "yn",
    "yr",
    "yth",
    "ae",
    "eon",
    "yra",
    "oros",
    "ythar",
    "eira",
    "uon"
]

ENDINGS += [
    # Short
    "e",
    "i",
    "o",
    "u",
    "er",
    "ur",
    "an",
    "en",
    "in",

    # Classic sci-fi
    "ian",
    "ira",

    # Elite-flavoured
    "ya",
    "yon",
    "th",

    # Exotic
    "asi",

    # Longer
    "anis",
    "oron",
    "oria",
    "aeon",
    "ythea",

    # Exotic
    "orus",
    "alon",
    "ador",
    "ath",
    "etha",
    "ovar",
    "amir",
    # Elite-flavoured
    "thea",
    # Exotic
    "ynos",
    "orax"
]



NUM_SYL1 = [
    "al", "bel", "cal", "del", "el", "fal",
    "gal", "hal", "kal", "mor", "nor", "sel",
    "tel", "val", "zar"
]

NUM_SYL2 = [
    "", "", "", "",

    # Single vowels
    "a", "e", "i", "o", "u", "y",

    # Traditional pairs
    "ae", "ai", "ao",
    "ea", "ei", "eo",
    "ia", "ie", "io",
    "oa", "oe", "oi",
    "ou",
    "ua", "ue", "ui", "uo",

    # Y combinations
    "ay", "ey", "iy", "oy", "uy",
    "ya", "ye", "yi", "yo", "yu",

    # More Elite-sounding
    "yae", "yea", "yia",
    "aey", "eya", "iya",
    "ayo", "eyo", "iyo",

    # Exotic combinations
    "au", "eu", "iu",
    "oae", "eou", "uae"
]

NUM_SYL3 = [
    "ra", "ron", "ria", "nus",
    "dor", "len", "mir", "th",
    "var", "thea", "ion"
]


def procedural_number_name(number: int) -> str:
    """
    Deterministically convert a sector number into
    a pronounceable pseudo-word.
    """

    h = hashlib.sha256(str(number).encode()).digest()

    return (
        ROOTS[h[0] % len(ROOTS)] +
        MIDDLES[h[1] % len(MIDDLES)] +
        ENDINGS[h[2] % len(ENDINGS)]
        # NUM_SYL1[h[0] % len(NUM_SYL1)] +
        # NUM_SYL2[h[1] % len(NUM_SYL2)] +
        # NUM_SYL3[h[2] % len(NUM_SYL3)]
    ).capitalize()


def humanise_sector(sector):
    result = []

    for token in sector.split():

        # Remove the word "Sector"
        if token.lower() == "sector":
            continue

        # Convert pure numbers
        if token.isdigit():
            result.append(procedural_number_name(int(token)))
        else:
            result.append(token)

    return " ".join(result)


def split_system_name(name):
    """
    Returns (sector, procedural_code)
    """
    parts = name.split()

    for i, part in enumerate(parts):
        if CODE_RE.match(part):
            return (
                " ".join(parts[:i]),
                " ".join(parts[i:])
            )

    return (name, "")


def name_from_code(code):
    """
    Generate a pronounceable name from a procedural code.
    Systems sharing the same family code tend to share roots.
    """

    tokens = code.split()

    if not tokens:
        # return "Prime"
        return ""

    family = tokens[0]
    instance = " ".join(tokens[1:])

    family_hash = hashlib.sha256(family.upper().encode()).digest()
    instance_hash = hashlib.sha256(instance.upper().encode()).digest()

    root = ROOTS[family_hash[0] % len(ROOTS)]

    middle = MIDDLES[
        ((instance_hash[0] << 8) | instance_hash[1])
        % len(MIDDLES)
    ]

    ending = ENDINGS[
        ((instance_hash[2] << 8) | instance_hash[3])
        % len(ENDINGS)
    ]

    return root + middle + ending


def humanise_system(system_name):
    """Return human-friendly name in place of bland procedurally coded name."""
    sector, code = split_system_name(system_name)

    sector = humanise_sector(sector)

    generated = name_from_code(code)

    return f"{sector} {generated}".strip()


def save_pair(first, second):
    """Append a pair of strings unless that exact pair is already stored."""
    pair = json.dumps([first, second], ensure_ascii=False)
    filename = "pair_database.lst"

    try:
        with open(filename, "r", encoding="utf-8") as database:
            if any(line.rstrip("\r\n") == pair for line in database):
                return
    except FileNotFoundError:
        pass

    with open(filename, "a", encoding="utf-8") as database:
        database.write(pair + "\n")


def get_other_name(name):
    """
    Find and return the paired value in pair_database.lst, or None.
    Allows back and forth translation without having to reverse
    hashing process.
    """
    filename = "pair_database.lst"
    name = name.casefold()

    try:
        with open(filename, "r", encoding="utf-8") as database:
            for line in database:
                try:
                    pair = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if not isinstance(pair, list) or len(pair) != 2:
                    continue
                if isinstance(pair[0], str) and pair[0].casefold() == name:
                    return pair[1]
                if isinstance(pair[1], str) and pair[1].casefold() == name:
                    return pair[0]
    except FileNotFoundError:
        pass

    return None



if __name__ == "__main__":

    sysname = sys.argv[1]

    verbose = True

    # see if we already have the system name (raw or humanised) in the database,
    # if not then assume a raw name has been given and humanise it
    paired_name = get_other_name(sysname)
    if paired_name is not None:
        if verbose: print("alternate name retrieved from database:")
        print(paired_name)
    else:
        if verbose: print("not in database, humanising:")
        humanised = humanise_system(sysname)
        print(humanised)
        if sysname != humanised:
            save_pair(sysname, humanised)



