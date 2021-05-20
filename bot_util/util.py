__all__ = ('split_line',)


def split_line(string: str, num: int)-> list[str]:
    str1, str2 = string[:num], string[num:]
    str1_split = str1.splitlines()
    str1, str12 = ''.join(str1_split[:-1]), str1_split[:-1]
    str2 = str12 + str2
    splited = [str1, str2]
    if len(str2) > num:
        splited.extend(split_line(str2, num))
    return splited
