from ui.text_wrap import wrapLineToWidth, wrapLinesToWidth


def measureTenPixelsPerCharacter(text):
    """Stand-in for a font's width measurement: every glyph is 10px wide.

    Keeps the wrapping assertions readable and independent of the real
    freesansbold metrics, which the rendering tests cover instead.
    """
    return len(text) * 10


def test_short_line_is_left_alone():
    assert wrapLineToWidth("one two", measureTenPixelsPerCharacter, 100) == ["one two"]


def test_long_line_is_split_on_word_boundaries():
    line = "the ophidian died"
    # "the ophidian" is 120px, "the ophidian died" is 170px
    assert wrapLineToWidth(line, measureTenPixelsPerCharacter, 130) == [
        "the ophidian",
        "died",
    ]


def test_every_wrapped_line_fits_the_width():
    line = "The ophidian Jormungandr lived to level 1, before its own hand."
    for wrapped in wrapLineToWidth(line, measureTenPixelsPerCharacter, 200):
        assert measureTenPixelsPerCharacter(wrapped) <= 200


def test_empty_line_survives_as_a_separator():
    assert wrapLineToWidth("", measureTenPixelsPerCharacter, 100) == [""]


def test_word_wider_than_the_width_gets_its_own_line():
    # nothing can be done for it but keep it whole - splitting mid-word or
    # dropping it would both cost more than the clipping does
    assert wrapLineToWidth(
        "hi supercalifragilistic bye", measureTenPixelsPerCharacter, 50
    ) == ["hi", "supercalifragilistic", "bye"]


def test_wrap_lines_flattens_each_wrapped_line_in_order():
    lines = ["== Obituary ==", "one two three four", "", "Total runs: 3"]
    assert wrapLinesToWidth(lines, measureTenPixelsPerCharacter, 150) == [
        "== Obituary ==",
        "one two three",
        "four",
        "",
        "Total runs: 3",
    ]
