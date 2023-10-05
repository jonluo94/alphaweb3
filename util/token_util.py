import hashlib
import os


def check_token(token: str):
    current_path = os.path.dirname(os.path.dirname(__file__))
    token_file = os.path.join(current_path, "token", token)
    return os.path.exists(token_file)


def init_token(user_name: str):
    # 要加密的数据
    data = f"alphaweb3-{user_name}"

    hashed = hashlib.md5(data.encode())
    user_secret = hashed.hexdigest()

    tk = f"alphaweb3-{user_name}-{user_secret}"
    sha256 = hashlib.sha256()
    sha256.update(tk.encode('utf-8'))
    token_value = sha256.hexdigest()

    current_path = os.path.dirname(os.path.dirname(__file__))

    with open(os.path.join(current_path, "token", token_value), 'w') as f:
        f.write(f'{user_name}:{user_secret}')

    print(user_name, user_secret, token_value)