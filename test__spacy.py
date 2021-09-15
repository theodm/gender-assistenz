from pgender._spacy import spacify_with_coref


def test_spacify_with_coref():
    doc = spacify_with_coref("Er geht sein Eis essen.")

    doc._.coref_chains.print()
