from base64 import b64decode

gate = [118, 140, 231, 176, 205, 480, 308, 872, 702, 820, 1034, 1176, 1339, 1232, 1605, 1792, 782, 810, 1197, 880, 924,
        1694, 2185, 2208, 2775]
part_1 = [chr((num+7*i)//i) for i, num in enumerate(gate, 1)]
part_1.reverse()

block = b'c3MxLnRkMy57XzUuaE83LjVfOS5faDExLkxfMTMuR0gxNS5fTDE3LjNfMTkuMzEyMS5pMzIz'
hammer = [chunk[:2] for chunk in b64decode(block).decode().split('.')]
part_2 = [chunk[0] for chunk in hammer] + [chunk[1] for chunk in hammer] + ['']

flag = ''.join(p1 + p2 for p1, p2 in zip(part_1, part_2))
print(flag)  # vsctf{Th353_FL4G5_w3r3_inside_YOU_th3_WH0L3_T1M3}
