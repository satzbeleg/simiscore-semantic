import pytest

from app.validate_input import get_long_sentence_ids


@pytest.fixture
def sentences():
    return [
        "Einen Brief quer durch die USA schicken – in nur 10 Tagen!",
        "Eine revolutionäre Entwicklung, dauerte der Postversand um 1850 \
    doch ein bis zwei Monate.",
        "Möglich machte es der sogenannte Pony-Express.",
        "Am 3. April 1860 begann eine Stafette furchtloser junger Männer, \
    Briefe entlang der mehr als 3000 km langen Strecke zwischen Kalifornien \
    und Missouri zuzustellen – hoch zu Ross, den widrigen Wetterverhältnissen \
    und feindlichen Überfällen trotzend.",
        "Allem Pioniergeist zum Trotz schienen die Gründer jedoch aufs \
    falsche Pferd gesetzt zu haben.",
        "Denn bereits 18 Monate später wurde der Pony-Express eingestellt.",
        "Zwei Tage, nachdem das erste transkontinentale Telegramm per \
    Telegraf verschickt wurde.",
    ]


def test_short_sentences_no_truncation(sentences):
    sentences_dict = dict(zip(range(len(sentences)), sentences))
    truncated_sents = get_long_sentence_ids(sentences_dict)
    assert truncated_sents == []


def test_long_sentences_truncation(sentences):
    long_sent = " ".join(sentences).replace(".", " ")
    sentences.insert(0, long_sent)
    truncated_sent_ids = get_long_sentence_ids(
        dict(zip(range(len(sentences)), sentences))
    )
    assert truncated_sent_ids == [0]
