import hashlib
import os
import time
from datetime import datetime


class TokenBalance:
    user_name: str
    balance: int
    last_time: float

    def __init__(self, user_name: str, balance, last_time: float):
        self.user_name = user_name
        self.balance = balance
        self.last_time = last_time


all_token_balance = {}


def check_token(token: str):
    current_path = os.path.dirname(os.path.dirname(__file__))
    token_file = os.path.join(current_path, "token", token)
    return os.path.exists(token_file)


def check_token_balance(token: str):
    user, balance = get_token(token)
    if balance > 0:
        return True
    return False


def no_same_day(timestamp1, timestamp2):
    d1 = datetime.fromtimestamp(timestamp1)
    d2 = datetime.fromtimestamp(timestamp2)
    nosame = d1.date() != d2.date()
    return nosame


def get_token(token: str):
    now = time.time()
    # 不存在或者不是同一天则重置次数
    if (all_token_balance.get(token) is None) or no_same_day(all_token_balance[token].last_time, now):
        current_path = os.path.dirname(os.path.dirname(__file__))
        token_file = os.path.join(current_path, "token", token)
        with open(token_file, 'r') as file:
            contents = file.read()
            print(contents)
            resp = contents.split(":")
            all_token_balance[token] = TokenBalance(resp[0], int(resp[2]), now)

    # 计算
    tb = all_token_balance[token]
    return tb.user_name, tb.balance


def compute_token_balance(token: str):
    tkbal = all_token_balance[token]
    balance = tkbal.balance - 1
    tkbal.balance = balance
    all_token_balance[token] = tkbal
    # 计算
    return balance


def init_token(user_name: str):
    # 要加密的数据
    default_balance = 10
    data = f"alphaweb3-{user_name}"

    hashed = hashlib.md5(data.encode())
    user_secret = hashed.hexdigest()

    tk = f"alphaweb3-{user_name}-{user_secret}"
    sha256 = hashlib.sha256()
    sha256.update(tk.encode('utf-8'))
    token_value = sha256.hexdigest()

    current_path = os.path.dirname(os.path.dirname(__file__))

    with open(os.path.join(current_path, "token", token_value), 'w') as f:
        f.write(f'{user_name}:{user_secret}:{default_balance}')

    print(user_name, user_secret, token_value)
