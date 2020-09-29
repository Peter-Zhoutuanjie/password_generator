import hashlib
from getpass import getpass
import os
from aes_encryptor import AESEncryptor
from password_manager import PwdManager

def setting_admin():
    clear()
    pwd_manager = PwdManager(db_file)
    password = getpass("请设置管理密码\n")
    repassword = getpass("确认管理密码\n")
    if password == repassword:
        pwd_manager.create_admin(password)
        return password, pwd_manager
    else:
        print("两次输入不相同")
        exit(0)

if __name__ == '__main__':
    db_file = 'password_manager.db'
    admin_pwd = ''
    clear = lambda: os.system('cls')
    pwd_manager = None
    if os.path.isfile(db_file):
        pwd_manager = PwdManager(db_file)
        if pwd_manager.is_admin():
            password = getpass("请输入管理密码\n")
            if pwd_manager.vertify_admin(password):
                admin_pwd = password
                print('登录成功')
            else:
                print('密码错误')
                exit(0)
        else:
            admin_pwd, pwd_manager = setting_admin()
    else:
        admin_pwd, pwd_manager = setting_admin()

    key = hashlib.md5(admin_pwd.encode(encoding='UTF-8')).hexdigest()
    enc = AESEncryptor(key.encode('utf-8'))
    while True:
        input1 = input("按任意键继续...")
        clear()
        print("\n" + "*" * 15)
        print("Commands:")
        print("q = 退出程序")
        print("g = 获取账号密码")
        print("ga = 获取所有账号密码")
        print("add = 存储账号密码")
        print("up = 更新密码")
        print("de = 删除服务密码")
        print("batch_add_ip = 批量添加服务器ip: ip_list.txt")
        print("batch_store = 批量存储账号密码: pass_list.txt 空格分割")
        print("*" * 15)
        input_ = input(":")

        if input_ == "q":
            pwd_manager.close_db()
            print("\n再见！\n")
            break

        elif input_ == "add":
            pwd_manager.store(enc)

        elif input_ == "g":
            pwd_manager.get(enc)

        elif input_ == "up":
            pwd_manager.update(enc)

        elif input_ == "de":
            pwd_manager.delete(enc)

        elif input_ == "ga":
            pwd_manager.get_all(enc)

        elif input_ == "batch_add_ip":
            pwd_manager.batch_add_ip(enc)

        elif input_ == "batch_store":
            pwd_manager.batch_store(enc)

        else:
            print("Invalid command.")
