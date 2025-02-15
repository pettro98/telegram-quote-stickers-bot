from PIL.ImageFont import FreeTypeFont
import uniseg.linebreak
import uniseg.graphemecluster


def _try_add_grapheme_to_line(line: str, grapheme: str, font: FreeTypeFont, max_width: float) -> tuple[str, float, bool]:
    new_line = line + grapheme
    new_length = font.getlength(new_line)

    if new_length <= max_width:
        return new_line, new_length, True
    else:
        return line, 0, False  # return 0 length to save compute time


def _add_word_to_line(line: str, word: str, font: FreeTypeFont, max_width: float) -> tuple[list[str], float]:
    new_line = line + word

    # if line fits into given space, return it in an array
    if (new_length := font.getlength(new_line)) <= max_width:
        return [new_line], new_length

    # if added word fits into required space, return initial line and word
    if (word_len := font.getlength(word)) <= max_width:
        return [line, word], max(word_len, font.getlength(line))

    # else - word doesn't fit on a line - append graphemes to initial line until it exceeds max_width
    grapheme_units = uniseg.graphemecluster.grapheme_clusters(word)
    result_lines = []
    new_line = line
    max_length = font.getlength(line)
    for gr in grapheme_units:
        new_line, assumed_length, success = _try_add_grapheme_to_line(new_line, gr, font, max_width)
        if success:
            max_length = max(max_length, assumed_length)
        else:
            # this can not happen, right?... *padme.jpg*
            # assert len(font.getlength(gr)) > max_width, "UNEXPECTED: Cannot fit a single grapheme in line"
            result_lines.append(new_line)
            new_line = gr

    if new_line != "":
        result_lines.append(new_line)

    return result_lines, max_length


def _line_width_wrap(line: str, font: FreeTypeFont, max_width: float) -> tuple[list[str], int]:
    result_lines = []
    max_length = 0
    current_line = ""

    for word in uniseg.linebreak.line_break_units(line):
        fit_lines, assumed_length = _add_word_to_line(current_line, word, font, max_width)
        result_lines.extend(fit_lines[:-1])  # if word fits in current_line then extend by empty slice
        current_line = fit_lines[-1]
        max_length = max(max_length, assumed_length)

    if current_line != "":
        result_lines.append(current_line)

    return result_lines, max_length


def text_wrap(text: str, font: FreeTypeFont, max_width: int) -> tuple[list[str], int]:
    result_lines = []
    max_length = 0

    for line in text.splitlines():
        if line == "":  # just append empty lines, probably they are for formatting purpose
            result_lines.append("")
            continue

        fit_lines, fit_line_width = _line_width_wrap(line, font, max_width)
        result_lines.extend(fit_lines)
        max_length = max(max_length, fit_line_width)

    return result_lines, max_length
