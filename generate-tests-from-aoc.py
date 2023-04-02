#!/usr/bin/env python3

# Uses https://pypi.org/project/advent-of-code-data/
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from aocd.exceptions import PuzzleUnsolvedError
from aocd.models import Puzzle, User

sessions_file = f"{Path.home()}/.advent-of-code.json"
with open(sessions_file) as f:
    SESSIONS = json.load(f)

# Prevent webbrowser.open, which aocd calls, from opening a browser:
os.environ["BROWSER"] = "true"

if "AOC_YEAR" in os.environ:
    years_string = os.environ["AOC_YEAR"]
    if "-" in years_string:
        (years_start, years_end) = years_string.split("-")
        years = range(int(years_start), int(years_end) + 1)
    else:
        years = [int(years_string)]
else:
    years = range(2015, 2023)

if "AOC_DAY" in os.environ:
    days_string = os.environ["AOC_DAY"]
    if "-" in days_string:
        (days_start, days_end) = days_string.split("-")
        days = range(int(days_start), int(days_end) + 1)
    else:
        days = [int(days_string)]
else:
    days = range(1, 26)

if "AOC_PART" in os.environ:
    parts = [int(os.environ["AOC_PART"])]
else:
    parts = range(1, 3)

if "AOC_ACCOUNT" in os.environ:
    account = os.environ["AOC_ACCOUNT"]
else:
    account = "*"

generated_file = open(
    "app/src/test/java/advent/of/code/java/user/GeneratedTest.java", "w"
)

print(
    """package advent.of.code.java.user;

import net.fornwall.aoc.Solver;
import net.fornwall.aoc.SolverException;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class GenerateTest {
""",
    file=generated_file,
)


def escape_and_quote_string(s):
    def escape_string(s):
        return s.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')

    if len(s) < 50000:
        return '"' + escape_string(s) + '"'

    max_len = 50000
    chunks = [s[i : i + max_len] for i in range(0, len(s), max_len)]

    result = "new StringBuilder("
    first = True
    for chunk in chunks:
        if first:
            first = False
        else:
            result += ".append("
        result += '"' + escape_string(chunk) + '")'
    result += ".toString()"

    return result


for year in years:
    print(f"    @Test void solvesOfficialAnswers{year}() {{", file=generated_file)
    for day in days:
        cached_inputs = {}
        for session in SESSIONS:
            session_cookie = session["cookie"]
            if session_cookie == "TODO":
                continue
            session_description = session["description"]
            if not (account == "*" or account == session_description):
                continue

            user = User(session_cookie)

            print(f"# Year {year}, Day {day} - {session_description}", file=sys.stderr)
            puzzle = Puzzle(year=year, day=day, user=user)
            input_data = puzzle.input_data

            if input_data in cached_inputs:
                print(
                    "Skipping - input already seen for " + cached_inputs[input_data],
                    file=sys.stderr,
                )
                continue
            cached_inputs[input_data] = session_description

            for part in parts:
                if day == 25 and part == 2:
                    continue
                answer = puzzle.answer_a if part == 1 else puzzle.answer_b
                escaped_answer = escape_and_quote_string(answer)
                escaped_input = escape_and_quote_string(input_data)
                print(
                    f"        Assertions.assertEquals({escaped_answer}, Solver.solve({year}, {day}, {part}, {escaped_input}));",
                    file=generated_file,
                )
    print("    }\n", file=generated_file)

print("}", file=generated_file)
