from pgender.pipeline.full_pipeline import full_pipeline


def test_full_pipeline():
    res = full_pipeline("""Frühaufsteher, Radfahrer und zu 100 Prozent loyal: Söders Machtzirkel besteht aus einem sorgsam ausgewählten Kreis an langjährigen Vertrauten. Wer gehört dazu? Heute ist ihr Chef im ARD-Sommerinterview.""")

    print(res)
