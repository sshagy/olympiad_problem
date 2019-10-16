from itertools import groupby
from collections import Counter
import re

def divariate(x: int) -> int:
    res = 0
    m = x
    while x > 0:
        res += m
        x, m = divmod(x, 10)
    res += m
    return res

N = 10000000  # 100042, {'11:7', '15:1', '2:4', '2:1', '28:1', '11:9', '11:8'}
print(f'N: {N}')
# отсортированный список производных чисел
# P = sorted([divariate(i) for i in range(N)])
P = set(divariate(i) for i in range(N))
# print(f'P: {P}')
print(f'P: {len(P)}')

# список самопроизводны (в разы меньше)
SP = [x for x in range(max(P)) if x not in P]
# print(f'SP: {SP}')
print(f'SP: {len(SP)}')
print(f'P + SP: {len(P) + len(SP)}')

# вычисление дельты для последовательности
D = [SP[i + 1] - SP[i] for i in range(len(SP) - 1)]
# print(D)

# LRE сжатие для дельт
C = [
    '{}:{}'.format(key, len(tuple(group)))
    # (key, len(tuple(group)))
    for key, group in groupby(D)
]
# print(C)

#
UC = set(C)         # набор уникальных сжатых дельт
FC = Counter(C)     # частотный словарь
AC = {              # шифратор
    x: chr(ord('a') + i)
    for i, x in enumerate(
        sorted(FC, key=lambda x: FC[x], reverse=True))
}

print(UC)
FC_values = tuple(FC.values())
FC_avg = sum(FC_values) / len(FC_values)
FC_term = ''.join(
    AC[x]
    for x, v in sorted(FC.items(), reverse=True)
    if v > FC_avg
)
AC[FC_term] = chr(ord(max(AC.values())) + 1)
print(FC, FC_values, FC_avg, FC_term)
ACR = {v: k for k, v in AC.items()}  # дешифратор
print(AC, ACR)

# зашифрованный список сжатых дельт самопроиздодных чисел (но дадее будем еще сжимать закодированный список)
CC = ''.join(AC[x] for x in C)
# print(CC)

# сжимаем этот зашифрованный список
# ebababababababababacdcababababababababacdcababababababababacdcababababababababacdcababababababababacdcababababababababacdcababababababababacdcababababababababacdcababababababababacdcabababababababababe
# new term: ab => f
# eb8facdc8f...
compress_num = lambda l: l if l > 1 else ''
CCC = re.sub(FC_term, AC[FC_term], CC)
CCC = ''.join(
    f'{compress_num(len(tuple(group)))}{key}'
    for key, group in groupby(CCC)
)
# print(CCC)

# TODO: автоматизировать нахождение нового терма и дальнейшее сжатие
# сжимаем еще раз,например для 50000
# gb8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8haefe8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8haefe8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8haefe8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8haefe8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc8hacdc9hg
# new term: 8hacdc => i
# gb9i8haefe9i8haefe9i8haefe9i8haefe9hg
# new_term = '8jacdc'  # for 10**6
new_term = '8lacdc' # for 10**7
AC[new_term] = chr(ord(max(AC.values())) + 1)
CCCC = re.sub(new_term, AC[new_term], CCC)
CCCC = ''.join(
    f'{compress_num(len(tuple(group)))}{key}'
    for key, group in groupby(CCCC)
)
# print(CCCC)

# упарываемся и сжимаем еще раз, например длая тех же 50000
# gb9i8haefe9i8haefe9i8haefe9i8haefe9hg
# new term: 9i8haefe => j
# gb4j9hg
# new_term = '9k8jaefe' # for 10**6
new_term = '9m8laefe' # for 10**7
AC[new_term] = chr(ord(max(AC.values())) + 1)
CCCCC = re.sub(new_term, AC[new_term], CCCC)
CCCCC = ''.join(
    f'{compress_num(len(tuple(group)))}{key}'
    for key, group in groupby(CCCCC)
)
# print(CCCCC)
# print(AC)

# ib9l9k8jaghg9l9k8jaghg9l9k8jaghg9l9k8jaghg9l9k8jaghg9l9k8jaghg9l9k8jaghg9l9k8jaghg9l9k8jaghg9l9k9ji
new_term = '9n9m8laghg' # for 10**7
AC[new_term] = chr(ord(max(AC.values())) + 1)
CCCCCC = re.sub(new_term, AC[new_term], CCCCC)
CCCCCC = ''.join(
    f'{compress_num(len(tuple(group)))}{key}'
    for key, group in groupby(CCCCCC)
)
print(CCCCCC)
print(AC)

# результирующий список самопроизводных(True) и чисел генераторов (False).
# то что выше делать не обязательно, если придумать как воспроизводить список `C` линейной сложностью.
sp = 1  # первое самопроизводное число
i = 0
RES = []
# for item in C:
for item in CC:
    item = ACR[item]  # дешифруем
    k, l = map(int, item.split(':')) # получаем данные для декомпрессии LRE
    for _ in range(l):
        RES.extend([0] * (sp - i))  # False - число генератор
        i = sp + 1
        RES.append(1)  # True - самопроизводное число
        sp += k

# print(f'RES: {RES}')
print(f'RES: {len(RES)}')
