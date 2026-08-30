# @author Claude
# @since August 29th, 2026

"""Width-aware word wrapping for the pygame UI.

Graphik.drawText centres a whole string on the point it is given and neither
wraps nor shrinks it, so a line wider than the window loses an equal share off
both ends. The obituary screen - so far the only one that draws a whole
sentence rather than short labels - wraps its lines through here first.

Measuring is left to the caller as a `measureWidth(text) -> int` callable so
the wrapping itself stays a pure function of text and numbers - the caller
passes the same font Graphik will render with, and the tests can pass a
predictable stand-in instead of pinning down glyph metrics.
"""


def wrapLineToWidth(line, measureWidth, maxWidth):
    """Greedily wraps one line onto as many lines as its words need.

    An empty line survives as an empty line (the obituary screen uses one as
    a section separator), and a single word too wide to fit anywhere is left
    over-wide on a line of its own rather than being split mid-word or
    dropped - clipping one word is better than losing the sentence.
    """
    if not line:
        return [line]
    wrapped = []
    current = ""
    for word in line.split(" "):
        candidate = word if not current else current + " " + word
        if current and measureWidth(candidate) > maxWidth:
            wrapped.append(current)
            current = word
        else:
            current = candidate
    wrapped.append(current)
    return wrapped


def wrapLinesToWidth(lines, measureWidth, maxWidth):
    """Wraps each line in a list, flattened back into one list of lines."""
    wrapped = []
    for line in lines:
        wrapped.extend(wrapLineToWidth(line, measureWidth, maxWidth))
    return wrapped
