__all__ = ('YAML_DUMP_CONFIG','split_line')


YAML_DUMP_CONFIG = {
    'encoding':'utf8',
    'allow_unicode':True,
    'default_flow_style':False
    }


def split_line(string: str, num: int)-> list[str]:
    string, num = str(string), int(num)
    if len(string) <= num:
        return [string]
    str1, str2 = string[:num], string[num:]
    str1_split = str1.splitlines(keepends=True)
    if len(str1_split) > 1:
        str1 = ''.join(str1_split[:-1])
        str2 = str1_split[-1] + str2
    splited = [str1]
    if len(str2) > num:
        splited.extend(split_line(str2, num))
    else:
        splited.append(str2)
    return splited
