def __VLI(n):
    # 获取整数n的可变字长整数编码
    ts, tl = 0, 0
    if n > 0:
        ts = bin(n)[2:]
        tl = len(ts)
    elif n < 0:
        tn = (-n) ^ 0xFFFF
        tl = len(bin(-n)[2:])
        ts = bin(tn)[-tl:]
    else:
        tl = 0
        ts = '0'
    return (tl, ts)

def __IVLI(tl, ts):
    # 获取可变字长整数编码对应的整数n
    if tl != 0:
        n = int(ts, 2)
        if ts[0] == '0':
            n = n ^ 0xFFFF
            n = int(bin(n)[-tl:], 2)
            n = -n
    else:
        n = 0
    return n

if __name__ == '__main__':
    num = -23
    print(__VLI(num))