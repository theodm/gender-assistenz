# Gibt die Kinder zurück, die mit einer bestimmten
# Relationseigenschaft (app, ...) verbunden sind.
def follow_child_dep(word, rel):
    if type(rel) is not list:
        rel = [rel]

    result = []
    for child in word.children:
        if child.dep_ in rel:
            result.append(child)

    return result


# Gibt maximal ein Kind zurück, welches mit einer bestimmten
# Relationseigenschaft (app, ...) verbunden sind.
def follow_child_dep_single_or_none(word, rel):
    result = follow_child_dep(word, rel)

    if len(result) > 1:
        raise Exception(f"Es darf nur ein Element mit dieser Beziehung geben. ({word} mit {rel}, war aber {result})")

    if not result:
        return None

    return result[0]

# Gibt das Elternteil zurück, wenn dieses mit einer bestimmten
# Relationseigenschaft (app, ...) verbunden ist, ansonsten None.
def follow_parent_dep(word, rel):
    if type(rel) is not list:
        rel = [rel]

    if word.dep_ in rel:
        return word.head

    return None