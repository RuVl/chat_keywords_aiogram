import re
import string

chars = f'[{re.escape(string.punctuation)}]'


def parse_text(text: str) -> set[str]:
    words = re.sub(chars, '', text.lower()).split()
    return set(map(str.strip, words))


def parse_keywords(parse_string: str | None) -> set[str]:
    if parse_string is None:
        return set()

    keywords = parse_string.strip().lower().split(';')
    return set(map(str.strip, keywords))


# Parse my syntax to regex syntax
def parse_condition(parse_string: str) -> str:
    and_prefix, and_sep, and_postfix = r'(?=.*', r')(?=.*', r')'
    or_prefix, or_sep, or_postfix = r'(?:', r'|', r')'

    parsed = []
    for expr in parse_string.split('^'):
        and_expr = and_prefix

        for condition in map(str.strip, expr.split('->')):
            if condition[0] != '[' or condition[-1] != ']':
                raise SyntaxError('Must be brackets around expression!')

            if len(condition) < 3:
                raise SyntaxError('No bracketed expression!')

            words = list(map(str.strip, condition[1:-1].split('|')))

            if len(words) == 1:
                if not words[0]:
                    raise SyntaxError(f"One of expression's part isn't contain words: {condition}")

                and_expr += words[0] + and_sep
                continue

            or_expr = or_prefix
            for word in words:
                if not word:
                    raise SyntaxError(f'Incorrect expression {condition}')

                or_expr += f'{word}{or_sep}'

            and_expr += or_expr[:-1] + or_postfix + and_sep

        and_expr = and_expr[:-len(and_sep)] + and_postfix
        parsed.append(and_expr)

    return '|'.join(parsed)  # Must be inserted around (?:{})
