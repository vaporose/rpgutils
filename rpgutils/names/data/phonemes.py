PHONEMES: dict[str, list[str]] = {
    # --- Part of speech ---
    "consonant": [
        "b", "p", "d", "t", "g", "k", "f", "v", "s", "z", "h",
        "m", "n", "l", "r", "w", "y", "x", "j",
        "sh", "th", "ch", "kh", "gh", "zh", "ng", "ts", "wh", "gn",
        "bl", "cl", "fl", "gl", "sl", "sm", "sn", "sw", "spl",
        "br", "cr", "fr", "pl", "pr", "sp", "st", "tw", "spr", "str", "scr",
        "dr", "tr", "gr", "kr", "zr", "hr", "skr", "thr", "vr", "kl",
        "nd", "nt", "ld", "lk", "nk", "rn", "rd", "rt", "rg",
    ],
    "vowel": [
        "a", "e", "i", "o", "u", "ï",
        "ae", "ai", "au", "ea", "ei", "ie", "ia",
        "oa", "oe", "ou", "ay", "ee", "oo", "ow", "oy", "aw",
    ],

    # --- Consonant manner of articulation ---
    "stop":      ["b", "p", "d", "t", "g", "k"],
    "fricative": ["f", "v", "s", "z", "h", "x", "sh", "th", "kh", "gh", "zh", "wh"],
    "nasal":     ["m", "n", "ng"],
    "liquid":    ["l", "r"],
    "glide":     ["w", "y"],
    "affricate": ["j", "ch", "ts"],

    # --- Consonant complexity ---
    "digraph": ["sh", "th", "ch", "kh", "gh", "zh", "ng", "ts", "wh", "gn"],
    "cluster": [
        "bl", "cl", "fl", "gl", "sl", "sm", "sn", "sw", "spl",
        "br", "cr", "fr", "pl", "pr", "sp", "st", "tw", "spr", "str", "scr",
        "dr", "tr", "gr", "kr", "zr", "hr", "skr", "thr", "vr", "kl",
        "nd", "nt", "ld", "lk", "nk", "rn", "rd", "rt", "rg",
    ],

    # --- Vowel type ---
    "short":     ["a", "e", "i", "o", "u", "ï"],
    "diphthong": ["ae", "ai", "au", "ea", "ei", "ie", "ia", "oa", "oe", "ou",
                  "ay", "ee", "oo", "ow", "oy", "aw"],

    # --- Tonal quality ---
    "soft": [
        "b", "f", "v", "s", "m", "n", "l", "r", "w", "y", "j",
        "sh", "th", "wh",
        "bl", "cl", "fl", "gl", "sl", "sm", "sn", "sw", "spl",
        "e", "i",
        "ae", "ai", "ea", "ei", "ie", "ia", "ee",
    ],
    "hard": [
        "d", "g", "k", "z", "x",
        "dr", "tr", "gr", "kr", "zr", "skr", "thr",
    ],
    "guttural": [
        "x", "kh", "gh", "zh", "gn",
        "gr", "kr", "zr", "hr", "skr",
        "rg",
    ],
    "dark": [
        "a", "o", "u", "ï",
        "au", "oa", "ou", "oo", "ow", "aw",
    ],
}
