import re
import string
from typing import Union

from core.database.models import SamDB

chars = f'[{re.escape(string.punctuation)}]'


def parse_text(text: str) -> set[str]:
    words = re.sub(chars, '', text.lower()).split()
    return set(map(str.strip, words))


def parse_keywords(parse_string: str) -> set[str]:
    keywords = parse_string.strip().lower().split(';')
    return set(map(str.strip, keywords))


# Add strings like: firstname, lastname - number
# Returns parsed SamDB or error string
def parse_sam_db(parse_string: str) -> Union[set[SamDB], str]:
    rows = parse_string.strip().split('\n')

    result = set()
    for row in rows:
        split = row.split(' - ')
        if len(split) != 2:
            return row

        name, number = split
        if not number.isdecimal():
            return row

        split = name.split(',')
        if len(split) > 2:
            return row
        elif len(split) == 2:
            first_name, last_name = split
            last_name = last_name.strip()
        else:
            first_name, last_name = split[0], None

        sam_db = SamDB(first_name=first_name.strip(), last_name=last_name, number=int(number))
        result.add(sam_db)

    return result


def parse_db_numbers(parse_string: str) -> Union[set[int], str]:
    rows = parse_string.strip().split('\n')

    result = set()
    for row in rows:
        split = row.split(' - ')
        if len(split) > 2:
            return row

        number = split[-1]
        if not number.isdecimal():
            return row

        result.add(int(number))

    return result
