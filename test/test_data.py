from dataclasses import dataclass

from bot_util import data

@dataclass
class test1:
    name: str

@dataclass
class test2:
    age: int

data.add_dataclass('test',test1).add_dataclass('test2',test2)

print(dir(data))
print(data.test)
print(data.test2)
print('start reload')
data.all_reload()
print('finish reload')
print(dir(data))
print(data.test)
print(data.test2)
