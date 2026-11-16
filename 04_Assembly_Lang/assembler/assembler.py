"""Hack assembler: translates a .asm file into a .hack file of 16-bit words.

REPLACEMENT NOTICE
    The original assembler was written for nand2tetris Project 6 and then
    lost; only an empty assembler.py survived. This file is a stand-in so the
    toolchain is whole again. It was written by an AI assistant, not by the
    repo's author, so read it as a placeholder, not as the original work.

Usage:
    python assembler.py Prog.asm            # writes Prog.hack next to it
    python assembler.py Prog.asm -o out.hack

Two passes, standard library only:
    1. record every (LABEL) at the ROM address of the instruction after it
    2. translate each instruction; an unknown @symbol becomes a variable,
       given the next free RAM address starting at 16
"""

import argparse
import sys
from pathlib import Path

# comp field: the a-bit plus c1..c6, keyed by mnemonic
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101",
}
# the commutative spellings (A+D, M&D, ...) mean the same thing
for _op in "+&|":
    for _reg in "AM":
        COMP[f"{_reg}{_op}D"] = COMP[f"D{_op}{_reg}"]

JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 0x4000, "KBD": 0x6000,
    **{f"R{i}": i for i in range(16)},
}

MAX_A_VALUE = 0x7FFF  # an A-instruction carries 15 bits
FIRST_VARIABLE = 16


class AsmError(Exception):
    """A malformed line, reported with its line number."""


def clean(line):
    """Strip the comment and every space: Hack has no meaningful whitespace."""
    return line.split("//", 1)[0].replace(" ", "").replace("\t", "").strip()


def parse(source):
    """Yield (line_number, instruction) for every non-empty line."""
    for number, raw in enumerate(source.splitlines(), start=1):
        text = clean(raw)
        if text:
            yield number, text


def is_symbol(name):
    """A symbol: letters, digits, _ . $ :, not starting with a digit."""
    allowed = set("_.$:")
    return bool(name) and not name[0].isdigit() and all(
        ch.isalnum() or ch in allowed for ch in name
    )


def first_pass(lines):
    """Map every (LABEL) to the ROM address of the next real instruction."""
    symbols = dict(PREDEFINED)
    rom_address = 0
    for number, text in lines:
        if text.startswith("("):
            if not text.endswith(")") or not is_symbol(text[1:-1]):
                raise AsmError(f"line {number}: bad label '{text}'")
            label = text[1:-1]
            if label in symbols:
                raise AsmError(f"line {number}: '{label}' defined twice")
            symbols[label] = rom_address
        else:
            rom_address += 1
    return symbols


def a_instruction(value, symbols, next_variable, number):
    """@value -> 0vvvvvvvvvvvvvvv. returns (word, next_variable)."""
    if value.isdigit():
        address = int(value)
        if address > MAX_A_VALUE:
            raise AsmError(f"line {number}: @{value} doesn't fit in 15 bits")
    elif is_symbol(value):
        if value not in symbols:
            symbols[value] = next_variable
            next_variable += 1
        address = symbols[value]
    else:
        raise AsmError(f"line {number}: bad A-instruction '@{value}'")
    return f"0{address:015b}", next_variable


def c_instruction(text, number):
    """dest=comp;jump -> 111a cccccc ddd jjj"""
    dest, _, rest = text.rpartition("=")
    comp, _, jump = rest.partition(";")

    if comp not in COMP:
        raise AsmError(f"line {number}: unknown computation '{comp}'")
    if jump not in JUMP:
        raise AsmError(f"line {number}: unknown jump '{jump}'")
    if len(set(dest)) != len(dest) or not set(dest) <= set("ADM"):
        raise AsmError(f"line {number}: bad destination '{dest}'")

    # d1 d2 d3 = A D M, in any order the source writes them
    dest_bits = "".join("1" if reg in dest else "0" for reg in "ADM")
    return f"111{COMP[comp]}{dest_bits}{JUMP[jump]}"


def assemble(source):
    """Translate Hack assembly text into a list of 16-character bit strings."""
    lines = list(parse(source))
    symbols = first_pass(lines)
    next_variable = FIRST_VARIABLE
    words = []

    for number, text in lines:
        if text.startswith("("):
            continue
        if text.startswith("@"):
            word, next_variable = a_instruction(
                text[1:], symbols, next_variable, number
            )
        else:
            word = c_instruction(text, number)
        words.append(word)
    return words


def main():
    parser = argparse.ArgumentParser(description="Hack assembler (.asm -> .hack)")
    parser.add_argument("source", type=Path, help="the .asm file")
    parser.add_argument("-o", "--output", type=Path, help="default: <source>.hack")
    args = parser.parse_args()

    output = args.output or args.source.with_suffix(".hack")
    try:
        words = assemble(args.source.read_text())
    except (AsmError, OSError) as error:
        print(f"assembler: {error}", file=sys.stderr)
        return 1

    output.write_text("".join(word + "\n" for word in words))
    print(f"{args.source} -> {output} ({len(words)} instructions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
