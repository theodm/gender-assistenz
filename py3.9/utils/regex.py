import re


def regex_nth_or_none(regex, text, n):
    matches = re.findall(regex, text)

    if not matches:
        return None

    matches = matches[0]

    if type(matches) is not tuple and n == 0:
        return matches

    if len(matches) <= n:
        return None

    return matches[n]


def regex_first_or_none(regex, text):
    return regex_nth_or_none(regex, text, 0)