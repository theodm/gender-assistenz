from pipeline.full_pipeline import full_pipeline
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

def test_full_pipeline_step3b():
    res = full_pipeline("""Fortschritt wird erreicht, wenn jeder volljährige Bürger, der eine Meinung hat, wählen geht.""")

    print(res)

def test_combination():
    res = full_pipeline("Der Benutzer sagte, er sei vorsichtig vorgegangen.")

    print(res)

def test_combination_2():
    res = full_pipeline("Der Benutzer sagte, er sei vorsichtig vorgegangen.")

    print(res)


def test_Beamte():
    res = full_pipeline("Angesichts der grenzüberschreitenden Mistproblematik beschäftigen sich in den Hauptstädten der beiden neutralen Nachbarländer bald mehr Beamte mit dem Mistkrieg als direkt betroffene Bauern.")

    print(res)

def test_Demonstranten():
    res = full_pipeline("""
Die Gläubigen hungern - und die Mullahs bereichern sich

Aufstände in mehreren Städten Irans kündigen die Spaltung zwischen dem Volk und den Herrschenden an
Von Ahmad Taheri

Kaum war der iranische Staatspräsident Ali Akhbar Rafsandschani aus den Parlamentswahlen als Sieger hervorgegangen, da brachen im Land soziale Unruhen aus.
Eine mächtige Welle des Aufruhrs überzog in den vergangenen Wochen die iranischen Städte.
Zum ersten Mal nach der Revolution rebellierten die Mostazafin, die "Schwachgehaltenen", wie die Armen in der Islamischen Republik genannt werden, gegen den schiitischen Gottesstaat.
Begonnen hatte die Rebellion der Armen in der südiranischen Stadt Schiras.
Am 7. April demonstrierten dort vier- bis fünfhundert Kriegsinvaliden gegen die Kürzung der ihnen zustehenden Lebensmittelrationen.
Als die Pasdaran, die Revolutionswächter, die Versammlung aufzulösen versuchten, kam es zu Handgreiflichkeiten, die sich rasch zu blutigen Krawallen in der ganzen Stadt ausdehnten.
Zwei Wochen später wiederholten sich die Ereignisse in der zentral gelegenen Stadt Arak, wo einst Ayatollah Khomeiny sein Theologiestudium angetreten hatte.
Der Anlaß für den Volkszorn war dieses Mal der Tod eines Kindes.
Ein achtjähriger Junge wurde am Rande der Stadt von einem Lastwagen überfahren, als die Polizei versuchte, die von Slumbewohnern unerlaubt gebauten Lehmhütten niederzureißen.
Tausende zogen ins Stadtzentrum und steckten alles in Brand, was nach staatlichen Einrichtungen aussah.
Vor den Augen der Pasdaran wurden die Bilder von Khomeiny, Khamenei und Rafsandschani wie die anderen Symbole der klerikalen Herrschaft von den Wänden heruntergerissen.
Erst mit Hilfe der aus anderen Orten herbeigeeilten Militäreinheiten und mit Verhängung des Ausnahmezustandes gelang es den lokalen Machthabern, der Lage Herr zu werden.
Seinen Höhepunkt erreichte der Aufstand der Mostazafin eine Woche später in Meschhed im Nordosten des Landes.
Auch hier löste die Auseinandersetzung um das unerlaubte Bauen, in deren Folge mehrere Menschen von einem Bulldozer zermalmt wurden, die blutigen Zusammenstöße aus.
Zehntausende Demonstranten trugen die Bahren der "Märtyrer" durch die Straßen der Zweimillionen-Stadt.
Polizeiwagen wurden mit Molotow-Cocktails beworfen, das staatliche Einkaufszentrum geplündert, Banken und Regierungsgebäude in Brand gesteckt.
Besonders in Mitleidenschaft geriet das Amt für "islamische Führung", nach offiziellen Angaben gingen hier Tausende von Koranexemplaren in Flammen auf.
Als zwei Wochen später eine Überschwemmung die Stadt heimsuchte, bezeichnete die Regimepropaganda die Naturkatastrophe als "Zorn Gottes gegen aufrührerische Frevler, die sich an Seinem Heiligen Buch versündigt "hatten.
Den Unruhen in der heiligen Stadt, wo Ali ar-Reza, der achte schiitische Imam, begraben ist, fielen dreißig bis vierzig Menschen zum Opfer.
"In Maschhad", reagierte der Revolutionsführer Ali Khamenei auf die Vorfälle in seiner Geburtsstadt, "war die Konterrevolution am Werke.
Sie benutzte die Lumpen, Asozialen, Dealer, Messerstecher, Schmarotzer und Geier für die eigenen Ziele".
Khamenei befahl den Revolutionsgerichten und den Revolutionswächtern, das "Unkraut erbarmungslos auszureißen".
Um diesen Auftrag schariagemäß zu erfüllen, erklärte der oberste Richter der Republik, Ayatollah Jazdi, die vermeintlichen Rädelsführer zu Mufsid fi al-Arz, den "Verderbern auf Erden".
Der Begriff bezeichnet vor allem die bewaffneten Staatsfeinde, denen nach der islamischen Rechtssprechung die Todesstrafe gilt.
Zehn von dreihundert verhafteten Demonstranten wurden in Schnellverfahren zur Todesstrafe verurteilt, vier von ihnen unmittelbar darauf hingerichtet.
Auch in Schiras wurden vier "Gottesfeinde" gehenkt.
Indessen wartete Staatspräsident Rafsandschani den Lauf der Dinge ab, bevor er sich zu Wort meldete.
Am 2. Juni räumte er vor dem Parlament ein, daß nicht die Volksmudschaheddin, die USA oder gar die radikalen Rivalen hinter den Unruhen stünden, wie es anfänglich von der offiziellen Propaganda behauptet wurde, sondern die soziale Not.
"Die Bevölkerung", sagte Rafsandschani, "ist mit einer Menge Probleme konfrontiert und daher unzufrieden.
Wir wissen alle, wie alarmierend die wirtschaftliche Lage ist, denn wir befinden uns in einer schwierigen Übergangsphase".
In der Tat ist die soziale Not zur Zeit schlimmer als je zuvor.
Das Sechzigmillionenvolk der Iraner ist trotz seiner natürlichen Reichtümer von Arbeitslosigkeit, Preissteigerung und Wohnungsnot geplagt.
Hinzu kommt, daß in der letzten Zeit eine Reihe der staatlichen Subventionen für die Grundnahrungsmittel abgeschafft worden sind, dank derer sich die arme Bevölkerung über Wasser halten konnte.
Während das gläubige Volk am Hungertuch nagt, wetteifern die Mullahs in Selbstbereicherung.
Viele von ihnen, die in Amt und Würde sind, haben inzwischen ein Vermögen zusammengerafft, von dem die Schahminister, deren Habgier sprichwörtlich war, nur träumen konnten.
Daß die Mostazafin, die einst den Mullahs zur Macht verholfen hatten, dies auf ewig nicht hinnehmen würden, war wohl zu erwarten.
Ihnen hatte Ayatollah Khomeiny nicht nur das Heil im Jenseits verheißen, sondern auch das Glück im Diesseits.
Der verstorbene Imam adelte die Armen zur "Krone der Schöpfung".
Gott habe den Mostazafin die Erde vererbt, verkündete er frei nach dem Koran.
In seinem Pariser Exil hatte Khomeiny dem Volk auf Heller und Pfennig vorgerechnet, was man alles mit Öldevisen für die "Schwachgehaltenen" tun könnte.
Der Krieg mit dem irakischen Nachbarland ermöglichte dem Imam, die Einlösung seiner Versprechen zu vertagen, ohne seine Glaubwürdigkeit gänzlich einzubüßen.
Mit dem Tod des Ayatollah wurde die Illusion von der künftigen islamischen Gerechtigkeit dann aber begraben.
Seine Erben hatten weder die Autorität noch die Glaubwürdigkeit, das Volk mit frommen Verheißungen abzuspeisen.
Die Armen, auf deren Rücken der achtjährige Krieg gegen Saddam Hussein geführt wurde, begannen langsam aber sicher, den Mullahs die Gefolgschaft zu versagen.
Die Reihen der Gläubigen beim Freitagsgebet, der polit-religiösen Nabelschau der klerikalen Macht, wurden immer lichter.
Und bei den jüngsten Parlamentswahlen gingen nur 26 Prozent der Stimmberechtigten zur Urne.
Der entflammte Zorn der eigenen Basis dürfte die Mullahs mehr in Schrecken versetzt haben als einst die Bomben der Volksmudschaheddin zu Beginn der islamischen Republik.
"Diese Ereignisse", sagte Rafsandschani im Parlament, "werden sich auch in Zukunft wiederholen.
Wir müssen darauf vorbereitet sein."
Vorbereitet werden zuallererst in Teheran effektivere Mittel der Gewalt.
In Schiras wie in Meschhed hatten sich die Revolutionsgardisten, die selbst aus den armen Schichten kommen, relativ zurückgehalten.
Jetzt sollen aus den Basidji, den linientreuen Freiwilligen, Antiterroreinheiten gebildet werden.
Ihr Name steht fest: "Aschura-Divisionen", genannt nach der höchsten schiitischen Märtyrerfeier.
Ob dies die Unzufriedenheit zu zügeln vermag, ist zweifelhaft.
Die langen Gefängnisstrafen, Auspeitschungen und Hinrichtungen der "Verderber auf Erden" konnten jedenfalls die Unruhen nicht eindämmen.
Kaum hatte das Radio die Vollstreckung der Todesurteile bekanntgegeben, ging der Sturm im Westen des Landes los.
In der kurdischen Stadt Bukan lieferte die Bevölkerung den Ordnungskräften zwei Tage lang regelrechte Straßenschlachten, nachdem ein Kaufmann von einem Revolutionsgardisten erschossen worden war.
Zuletzt kam es in Täbris, der zweitgrößten iranischen Stadt und der Metropole des persischen Aserbeidschan, zu Demonstrationen.
Zum ersten Mal ertönten neben den sozialen Forderungen auch Parolen von politischer Brisanz:
"Es lebe Groß-Aserbeidschan! "riefen die Demonstranten.
Bis jetzt hatten die iranischen Aseri allen Versuchungen widerstanden, nach Baku, der Hauptstadt des ehemals sowjetischen Aserbeidschan, zu schielen, wo der Traum von Groß-Aserbeidschan auf den Fahnen der regierenden Volksfront steht.
Vielen Jugendlichen bleibt nur Vereinzelung oder die Gruppe auf der Straße
Der Bielefelder Wissenschaftler Wilhelm Heitmeyer über die Ursachen von Gewalt in der jungen Generation und die Defizite der Politik
Professor Wilhelm Heitmeyer leitet das Projekt "Individualisierung und Gewalt "im Sonderforschungsbereich "Prävention und Intervention im Kindes- und Jugendalter" der Universität Bielefeld.
Er hat mehrere Studien zum Thema Rechtsextremismus und Gewalt veröffentlicht.
Seine neueste Langzeituntersuchung zur politischen Sozialisation männlicher Jugendlicher, die "Bielefelder Rechtsextremismus-Studie", ist gerade im Juventa-Verlag, Weinheim, erschienen.
Aus aktuellem Anlaß sprach mit ihm die Kölner FR-Korrespondentin Ingrid Müller-Münch.
FR: Was treibt Jugendliche dazu, sich gewalttätigen sogenannten Härtegruppen anzuschließen und im Kreise Gleichgesinnter loszuschlagen?
Heitmeyer: Ein zentraler Erklärungsansatz für die Entstehung von Gewalt sind für mich Desintegrations-Ängste und -Erfahrungen bei Jugendlichen.
Verunsicherung kommt etwa durch die Auflösung selbstverständlicher sozialer Zugehörigkeiten auf, wie sie zum Beispiel eine Trennung der Eltern mit sich bringt.
Dabei darf man sich allerdings nicht von der scheinbar größeren Intaktheit vollständiger Familien täuschen lassen.
Unsere Studie zeigt beispielsweise viele Variationen instrumentalisierter Umgehensweise hinter diesen Fassaden.
Jugendliche erfahren Unterstützung und Anerkennung etwa nur entsprechend der von ihnen gelieferten Leistung, zum Teil willkürlich, von Stimmung und Kalkül abhängig oder aber dadurch, daß man sich materiell freikauft von emotionalen Anstrengungen.
Ein ganz zentraler Faktor ist die Auflösung gemeinsam geteilter Zeit.
Das bedeutet, daß viele Sorgen, Nöte und Wünsche von Kindern und Jugendlichen häufig in den übrig gelassenen Zeitlücken der beruflich flexibilisierten Erwachsenen hineingestopft werden.
Solch tiefgreifende emotionale Bedürfnisse nach Zuhören, Zuwendung finden dann häufig keine unmittelbaren Anknüpfungspunkte.
Das betrifft übrigens Kinder und Jugendliche aus allen sozialen Milieus.
FR: Wo suchen sich diese Jugendlichen dann die überlebensnotwendige emotionale Zuwendung?
Heitmeyer: Das, was an öffentlichen Auffangmöglichkeiten zur Verfügung steht, etwa in Form von Ganztagsbetreuung in Kindertagesstätten, aber auch in Jugendeinrichten der offenen Tür oder betreuten Abenteuerspielplätzen, reicht jetzt schon nicht mehr.
Wenn dann, wie geplant, auch noch überall gespart werden soll, bleibt den Jugendlichen, die emotional nicht behaust sind, entweder die Vereinzelung oder die Gruppe auf der Straße.
Es öffnet sich derzeit eine gefährliche Schere zwischen gestiegenen Bedürfnissen nach emotionaler Nähe einerseits und Institutionen, die nur noch in der Lage sind zu "regeln" und zu verwahren.
FR: Hat das denn zur Folge, daß die Jugendlichen sich Orientierungen suchen außerhalb der bislang traditionellen Vorbilder aus Familie und Schule?
Heitmeyer: Ja, und zwar in den sogenannten Gleichaltrigengruppen.
Derartige Gruppen werden mit vielen Hoffnungen befrachtet, die sie möglicherweise gar nicht einlösen können.
Etwa dadurch, daß man selbst dort ständig unter Konkurrenzdruck steht, oder es auch mit der Solidarität untereinander vielfach nicht weit her ist.
Das betrifft vor allem jene Gruppen, die gegeneinander mit Gewalt vorgehen.
Gerade sie haben auch interne Gewaltprobleme.
FR: Wo treffen denn die Jugendlichen, die auf der Suche nach Orientierung sind, überhaupt auf Gleichaltrigengruppen?
Heitmeyer: Um sich als Jugendlicher eine Position zu verschaffen, ergeben sich zumeist drei Möglichkeiten:
Man kann diese Position über schulische Leistungen und Intelligenz erwerben, über Attraktivität und über Stärke.
Gerade die Schule ist reduziert darauf, daß man sprachlich gut drauf sein muß, in rationaler Beweisführung und Stil glänzen kann.
Wer darüber nicht verfügt, hat schlechte Karten.
Das bedeutet, daß man die Positionierung in anderen Bereichen suchen muß, und da bleibt häufig nur noch die Stärke-Demonstration.
FR: Treffen sich demnach in den Gruppen, die Gewalt ausleben, die sogenannten  Underdogs dieser Gesellschaft?
Heitmeyer: Wir müssen unterscheiden zwischen eher offenen physischen Gewaltformen, die sich über männlich dominierte Gruppen in der Öffentlichkeit zeigen, und solchen, eher psychischen Gewaltformen, die als Einzelaktivität eher mit einem hohen Bildungsgrad verbunden sind.
Die eine Form ist offenliegend, darauf reagieren wir.
Während die eher subtileren Formen vernachlässigt werden, weil sie besonders sozial akzeptiert sind und zur Grundausstattung der Gesellschaft gehören.
Zum Beispiel sind oftmals diejenigen, die sich in den Härtegruppen zusammentun, bei denen es um körperliche Gewaltausteilung geht, zuvor schon Opfer von subtilen Ausgrenzungen und Abwertungen geworden.
Und zwar auch von denjenigen, die sich so darstellen, als könnten sie keiner Fliege etwas zuleide tun, die aber massiv ihre Selbstdurchsetzung polieren.
Derjenige, der den Pythagoras nicht kapiert, wird mit Hohn und Spott seiner Klassenkameraden überschüttet und leidet unter Umständen darunter ebenso wie derjenige, der eine Tracht Prügel bezieht.
FR: Wird in diesem Bereich denn nun genügend geforscht, um Hintergründe der Gewalt bei Jugendlichen aufzudecken, damit mögliche Gegenmaßnahmen ergriffen werden können?
Heitmeyer: Leider nein.
Es gibt beispielsweise ein ausgeprägtes Desinteresse an intensiver Forschung zu jugendlichen Skinheads.
So ist das Bundesministerium von Frau Merkel nicht einmal in der Lage, beispielsweise einen größeren Forschungsantrag von uns zu jugendlichen Skinheads, der seit zweieinhalb Jahren vorliegt, abzulehnen.
Man tut einfach gar nichts.
Dies paßt durchaus in die politische Landschaft.
Denn je weniger man über die Hintergründe weiß, desto mehr kann man diese Jugendlichen funktionalisieren.
Und zwar von allen Seiten.
So können Skinheads und ihre Gewalttaten genutzt werden zur Begründung rigider Ausländerpolitik ebenso wie dazu, daß man sie als Barbaren tituliert, um seine eigene Politik von Fragen abzuschirmen.
Dabei sind gerade auch die Skinheads Kinder dieser Gesellschaft.
Sie zeigen uns gewissermaßen auf brutale Weise das Bild unserer eigenen gesellschaftlichen Zukunft, in der die Brutalität zunehmen wird.
Überall dort, wo sich soziale Verankerungen auflösen, müssen die Folgen des eigenen Handelns für andere nicht mehr sonderlich berücksichtigt werden.
Die Gewaltschwelle sinkt.

""")

    print(res)

def test_RossPerot():
    res = full_pipeline(""""Ross Perot wäre vielleicht ein prächtiger Diktator"

Konzernchefs lehnen den Milliardär als US-Präsidenten ab /
Texaner gibt nur vage Auskunft über seine Wirtschaftspolitik

Der texanische Milliardär Ross Perot hat das politische Establishment in Washington aufgeschreckt.
Nach Meinungsumfragen liegt der parteilose Self-mademan gut im Rennen um den Chefsessel im Weißen Haus mit dem amtierenden Präsidenten George Bush und dem Demokraten Bill Clinton.
Daß Perot ein Unternehmen erfolgreich leiten kann, davon sind selbst seine Kritiker überzeugt.
Ob diese Fähigkeiten aber ausreichen, um die größte Volkswirtschaft der Welt aus ihrer Krise zu führen, bezweifeln viele Ökonomen.
Und auch die Konzernchefs in den USA halten nicht viel von dem 62jährigen.
Zwar können sich die meisten Topmanager durchaus einen Unternehmer als Präsidenten vorstellen - nur nicht ausgerechnet Perot.
Nach einer Umfrage des Wirtschaftsmagazins Fortune unter den Bossen von 500 Großunternehmen wünschten im Mai nur elf Prozent "Ross for President", während 78 Prozent sich für Bush und vier Prozent für Clinton aussprachen.
Allerdings glaubt fast die Hälfte der Chief Executives, daß Perot durchaus Chancen habe, die Wahl im November zu gewinnen, wenn er denn kandidiert.
Als größte Schwäche des Texaners nennen die Befragten seinen Mangel an Erfahrung auf dem politischen Parkett.
Viele meinen, daß Perot mit seinem Befehlston auf dem Capitol gegen eine Wand laufen würde.
So erklärt etwa Edward Brandon von dem Unternehmen National City in Ohio:
"Ich glaube kaum, daß mit seinem, naja, etwas undiplomatischen Stil im Weißen Haus dem Land ein Gefallen getan wäre.
Er wäre vielleicht ein prächtiger Diktator - aber das ist nicht unser System."
Und ein anderer Manager vermutet, daß sich "ein Dogmatiker wie Perot in Washington schwer tun würde, es sei denn er schafft den Kongreß ab".
Ein ehemaliger Geschäftsführer, der heute in fünf Konzernen im Aufsichtsgremium sitzt, "kennt niemanden, der nicht glaubt, daß Perot als Präsident eine absolute Katastrophe wäre".
Allerdings gibt es dem Magazin zufolge in kleinen und mittleren Firmen viele Unternehmer, die meinen, Perot sei einer von ihnen, und die den Texaner unterstützen.
Zwei Themen, die Perot immer wieder anspricht, Rezession und Bürokratie, machen ihnen besonders zu schaffen.
Einer, der sich für den Milliardär ausspricht, ist Steve Jobs, dem Perot für den Aufbau der Computerfirma Next 20 Millionen Dollar bereitstellte.
Die Spekulationen darüber, welche Art Präsident "Henry der Hammer", so ein Spitzname aus Perots Jugendzeit, wäre, orientieren sich daran, wie Perot seine Milliarden machte.
Die Story geht so:
Mit 1000 von seiner Frau geborgten Dollar gründet der ehemalige IBM-Verkäufer 1962 die Electronic Data Services (EDS) und zeigt damit dem Rechnergoliath, daß es nicht nur gilt, Computer abzusetzen, sondern auch Geld damit zu verdienen ist, wenn man den Benutzern beim Einsatz der Maschinen hilft.
Das Informatik-Dienstleistungsunternehmen verkauft er 1984 für 2,5 Milliarden an General Motors.
Er tritt in die GM-Verwaltung ein und wird Großaktionär des Autokonzerns.
Ihm gelingt es aber nicht, den Koloß, der der Regierung in Washington mehr ähnelt als jeder andere Konzern, in Schwung zu bringen.
Nach zwei Jahren scheidet er dort aus, mit einer zusätzlichen GM-Zahlung von 700 Millionen Dollar in der Tasche.
Heutzutage hält Perot sein Vermögen vor allem in Staatspapieren und Immobilien.
Außerdem gehören ihm der Computer-Dienstleister Perot Systems, Beteiligungen an kleineren Firmen und persönliche Reichtümer wie Jachten, Jets und Villen.
Von modernem Management hat Perot, so Fortune, nie etwas gehalten.
Für ihn zählte allein "Führerschaft".
Von seinen Beschäftigten verlange er vor allem Arbeitsmoral und ordentliches Auftreten.
Perot sei ein autoritärer Macher, und das sei auch seine Schwäche, beschreibt ihn ein Manager.
Die Kritik der Ökonomenzunft an Perot entzündet sich vor allem an dessen vagen Äußerungen zur Wirtschaftspolitik.
"Es ist wirklich schwer zu sagen, welche Positionen er einnimmt, da er sich noch nicht konkret geäußert hat", beklagen Volkswirte.
Bisher bestehe sein "Programm "nur aus Allgemeinplätzen.
So will der politische Außenseiter beispielsweise das Steuersystem vereinfachen, das Bildungssystem verbessern, das gigantische Haushaltsdefizit abbauen, Einfuhren aus Japan drosseln und die geplante Freihandelszone der USA mit Mexiko verhindern.
Wie er diese Aufgaben lösen will, verrät er aber nicht.
Statt Details zu nennen, wiederholt er unverdrossen die "Erfolgsformel":
Die Amerikaner müssen hart arbeiten, um das Land wieder auf den richtigen Kurs zu bringen.
"Die Probleme unseres Landes sind doch weit größer als die eines Unternehmens", meint Rudy Oswald, Chefvolkswirt beim Gewerkschaftsbund AFL-CIO.
Schließlich sei die Regierung auch für die nationale Sicherheit und allgemeine Wohlfahrt verantwortlich.
"Hier geht es um mehr, als nur Profit zu machen", fügt er hinzu.
"Geschäftemachen ist seine Welt und nicht die Politik.
Er ist ein eigenwilliger Einzelgänger, der sich zudem nicht an Spielregeln hält", zeigt sich ein anderer Fachmann skeptisch.
Früher oder später, da sind sich alle einig, muß Perot Farbe bekennen und Konzepte vorlegen.
"Die Frage ist nur", meint ein Finanzexperte, "ob er ins Weiße Haus einziehen kann, ohne uns vorher zu sagen, was er eigentlich machen will."
sch / rtr""")

    print(res)
