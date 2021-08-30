from __future__ import annotations


from collections.abc import Generator
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import TypeVar, Union
    T = TypeVar('T')


__all__ = (
    'YAML_DUMP_CONFIG',
    'split_line',
    'get_unique_list',
    'maybe_int',
    'TimestampStyle',
    'format_dt',
    'docstring_updater',
    'utcnow',
)


YAML_DUMP_CONFIG = {
    'encoding': 'utf8',
    'allow_unicode': True,
    'default_flow_style': False
}


def split_line(string: str, num: int)-> Generator[str]:
    string, num = str(string), int(num)
    if len(string) <= num:
        yield string
        return
    str1, str2 = string[:num], string[num:]
    str1_split = str1.splitlines(keepends=True)
    if len(str1_split) > 1:
        str1 = ''.join(str1_split[:-1])
        str2 = str1_split[-1] + str2
    yield str1
    if len(str2) > num:
        yield from split_line(str2, num)
    else:
        yield str2


def get_unique_list(
        not_unique_list: list,
        *,
        need_flatten: bool= False
)-> list:
    if need_flatten:
        not_unique_list = sum(not_unique_list, [])
    return_list = []
    for element in not_unique_list:
        if element not in return_list:
            return_list.append(element)
    return return_list


def docstring_updater(doc):
    def deco(func):
        func.__doc__ += doc
        return func
    return deco


def maybe_int(obj: T)-> Union[int, T]:
    try:
        return int(obj)
    except Exception:
        return obj
