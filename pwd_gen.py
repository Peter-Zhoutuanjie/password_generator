import random


def pwd_generate(pwd_length):
    pwd_length = int(pwd_length)
    lChars = 'abcdefghijklmnopqrstuvwxyz'
    uChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '1234567890'
    specialChars = '!@#$%^&*-_+='
    seeds = [lChars, uChars, digits, specialChars]

    pre_pwd = {}
    # 每种类型字符随机取出一个
    for k in range(len(seeds)):
        seed = seeds[random.randint(0, len(seeds) - 1)]
        pre_pwd[k] = seed[random.randint(0, len(seed) - 1)]

    # 其余字符全部随机
    for i in range(len(seeds), pwd_length):
        seed = seeds[random.randint(0, len(seeds) - 1)]
        pre_pwd[i] = seed[random.randint(0, len(seed) - 1)]

    # 把取出来的字符全部重排
    sort_list = []
    for letter in pre_pwd.items():
        sort_list.append(letter[0])
    random.shuffle(sort_list)
    pwd = ''
    for i in sort_list:
        pwd += pre_pwd.get(i)
    return pwd

if __name__ == '__main__':
    pwd_generate(14)