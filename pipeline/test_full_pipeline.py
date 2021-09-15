from pgender.pipeline.full_pipeline import full_pipeline
#
# def test_full_pipeline_2():
#     res =

def test_full_pipeline():
    res = full_pipeline("""Frühaufsteher, Radfahrer und zu 100 Prozent loyal: Söders Machtzirkel besteht aus einem sorgsam ausgewählten Kreis an langjährigen Vertrauten. Wer gehört dazu? Heute ist ihr Chef im ARD-Sommerinterview.""")

    print(res)

def test_full_pipeline_ex1():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("Landtel ist nicht das erste Unternehmen , das als WLL-Anbieter scheitert")

def test_full_pipeline_ex2():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("Das schwäche nicht nur die Interessen der Aktionäre , sondern auch die der Arbeitnehmer und Gläubiger .")

def test_full_pipeline_ex3():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("Sollte ein Dienstanbieter die Kanäle einzeln weitervermieten , sind damit nach den Vorstellungen der Telekom pro Kanal 160 Mark an Telekom-Vorleistungsgebühren fällig - , eine Summe , die weit über den von einigen Anbietern wie AOL geforderten Endkundentarifen von rund 50 Mark für eine Flatrate liegt .")

def test_full_pipeline_ex4():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("TelDaFax-Nachfolger mit neuen Angeboten")

def test_full_pipeline_ex5():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("Die Regulierungsbehörde für Telekommunikation und Post(RegTP) hat entschieden, dass die Telekom den XXL - Pauschaltarif weiter anbieten darf - unter der Voraussetzung, dass der Rosa Riese das Angebot nicht nur für ISDN -, sondern auch für Analog - Zugänge anbietet.")

def test_full_pipeline_ex6():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("In einem Bereich gab es in diesem Jahr keinen Sieger.")

def test_full_pipeline_ex7():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("Wie angekündigt trennte die Telekom auch diesen Anbieter vom Netz.")

def test_full_pipeline_ex8():
    # TODO
    # Soll einfach nur keine Exception werfen.
    full_pipeline("Betroffen waren laut BerlinWeb - Inhaber Clemens Gerth zirka 10.000 Kunden, die ihre Web - Domains über den Berliner Anbieter laufen lassen.")

def test_full_pipeline_ex9():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("Es würden aber auch Gespräche mit jedem anderen Anbieter geführt, der meine, ein entsprechendes Angebot machen zu können.")

def test_full_pipeline_ex10():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("Nach seiner Aussage würde zwar sein Buchhalter daran glauben , aber nicht seine Kinder - und die wüssten viel mehr vom Internet als er .")

def test_full_pipeline_ex11():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("""Nach Angaben der Freiburger " Aktionärsgemeinschaft Metabox " soll ein Berliner Immobilienunternehmer Kopf der Investorengruppe sein .""")

def test_full_pipeline_ex12():
    # Soll einfach nur keine Exception werfen.
    full_pipeline("""" Der Messeführer kann jedoch nicht nur über das Internet , sondern auch direkt vor Ort in den Handheld geladen werden " , sagte Oliver Leheis , Sprecher der Drupa Düsseldorf , zu c't .""")


