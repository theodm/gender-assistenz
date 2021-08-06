from loguru import logger
from charsplit import Splitter

from pgender.fnf import has_feminine_noun_form
from pgender.wordlib import follow_parent_dep

splitter = Splitter()

def find_initial_words(doc):
    result = []
    index = 0
    for word in doc:
        logger.debug(f"{word.text} : {word.pos_} : {word.tag_} : {word.morph} : {word.lemma_}")

        if word.pos_ == "NOUN" and word.morph.get("Gender") and word.morph.get("Gender")[0] == "Masc":
            if has_feminine_noun_form(word, False):
                result.append((word, index))
            elif has_feminine_noun_form(word, True):
                result.append((word, index))
            else:
                splits = splitter.split_compound(word.text)

                logger.debug(f"splits found: {splits}")

                if splits and has_feminine_noun_form(splits[0][-1], True):
                    result.append((word, index))

        elif word.pos_ == "PRON" and \
                word.morph.get("Gender") and \
                word.morph.get("Gender")[0] == "Masc" \
                and word.tag_ in ["PDS", "PIS", "PPER", "PPOSS", "PRELS", "PWS"]:
            result.append((word, index))

        index = index + 1
    #
    # logger.debug(f"Result before filtering: {result}")
    #
    # words_to_remove = []
    # for r in result:
    #     # Fall: Ist das Pronomen Subjekt eines Relativsatzes, der sich auf
    #     #       ein bereits gefundenes Wort bezieht?
    #     #
    #     #       Wenn ja, entfernen wir das Wort, da wir das Pronomen im Rahmen
    #     #       des anderen Worts betrachten.
    #     #
    #     #       Bsp.: Derjenige, der sich impfen lassen will, der sollte einen Krankheitstag wegen Impfnebenwirkungen einplanen.
    #     #             _________  ___
    #     #
    #     subject_parent = follow_parent_dep(r[0], "sb")
    #     if subject_parent:
    #         relative_clause_parent = follow_parent_dep(subject_parent, "rc")
    #
    #         if relative_clause_parent and relative_clause_parent in [x[0] for x in result]:
    #             words_to_remove.append(r)
    #             logger.debug(f"Remove: {r[0].text} (relative clause rule)")
    #
    #     # Fall: Ist das Pronomen ein wiederholendes Pronomen bezüglich eines anderen
    #     #       bereits ermittelten Pronomen?
    #     #
    #     #       Bsp.: Derjenige, der sich impfen lassen will, der sollte einen Krankheitstag wegen Impfnebenwirkungen einplanen.
    #     #             _________                               ___
    #     #
    #     repeated_parent = follow_parent_dep(r[0], "re")
    #     if repeated_parent and repeated_parent in [x[0] for x in result]:
    #         words_to_remove.append(r)
    #         logger.debug(f"Remove: {r[0].text} (repeated element rule)")
    #
    #     # Fall: Beschreibt das Pronomen ein verwendetes Nomen oder ein anderes Pronomen, dann markieren wir nur
    #     #       das Nomen.
    #     #
    #     #       Bsp.: Bundeswirtschaftsminister Werner Müller, derjenige, der davon profitiert, freut sich über solche Aussichten.
    #     #             _________________________                _________
    #     app_parent = follow_parent_dep(r[0], "app")
    #     if app_parent and app_parent in [x[0] for x in result]:
    #         words_to_remove.append(r)
    #         logger.debug(f"Remove: {r[0].text} (apposition rule)")
    #
    # return [x for x in result if x not in words_to_remove]

    return result