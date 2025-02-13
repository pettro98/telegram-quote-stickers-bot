from typing import Tuple
import re

from PIL.ImageFont import ImageFont
import uniseg.linebreak
import uniseg.graphemecluster

def _line_width_fit(line:str, font: ImageFont, max_width:int) -> Tuple[list[str], int]:
    fit_line = []
    overall_width = 0
    current_line = ""

    for word in uniseg.linebreak.line_break_units(line):
        mew_word_line = current_line + word
        if (line_len := font.getlength(mew_word_line)) <= max_width:
            current_line = mew_word_line
            overall_width = max(overall_width, line_len)
            continue

        # if new line exceeds max_width then apply line-break algorithm
        if len(current_line) != 0:  # if line contains symbols then append and start with new word
            fit_line.append(current_line)
            current_line = ""
            continue

        # current line is empty == we could not fit the first word -> switch to by-grapheme breaking
        grapheme_break_units = uniseg.graphemecluster.grapheme_clusters(word)
        for gr in grapheme_break_units:
            new_grapheme_line = current_line + gr
            if font.getlength(new_grapheme_line) <= max_width:
                current_line = new_grapheme_line
            else:
                assert len(new_grapheme_line) == 0, "UNEXPECTED: Cannot fit a single grapheme in line"
                fit_line.append(current_line)
                overall_width = max(overall_width, line_len)
                current_line = ""

    # if last iteration resulted in non-empty line, add it to list
    if len(current_line) != 0:
        fit_line.append(current_line)

    return fit_line, overall_width


def text_width_fit(text: str, font: ImageFont, max_width: int) -> Tuple[list[str], int]:
    fit_lines = []
    overall_width = 0

    for line in text.splitlines():
        if line == "":  # just append empty lines
            fit_lines.append("")
            continue

        fit_line, fit_line_width = _line_width_fit(line, font, max_width)
        fit_lines.extend(fit_line)
        overall_width = max(overall_width, fit_line_width)

    return fit_lines, overall_width
