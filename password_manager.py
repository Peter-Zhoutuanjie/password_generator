import hashlib
import sqlite3
from getpass import getpass
from pwd_gen import pwd_generate
import prettytable as pt


class PwdManager:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor_ = self.conn.cursor()
        try:
            self.conn.execute('''CREATE TABLE STORE
                            (SERVICE TEXT PRIMARY KEY NOT NULL,
                            USERNAME TEXT NOT NULL,
                            PASSWORD TEXT NOT NULL);
                            ''')
            self.conn.execute('CREATE TABLE administrator(PASSWORD TEXT NOT NULL);')
        except:
            pass

    def get_password(self,service_):
        command = 'SELECT * from STORE WHERE SERVICE = "' + service_ + '"'
        cursor = self.conn.execute(command)
        for row in cursor:
            username_ = row[1]
            password_ = row[2]
        return [username_, password_]


    def add_password(self,service_, username_, password_):
        command = 'INSERT INTO STORE (SERVICE,USERNAME,PASSWORD) VALUES("'+service_+'","'+username_+'","'+password_+'");'
        self.conn.execute(command)
        self.conn.commit()


    def update_password(self,service_, password_):
        command = 'UPDATE STORE set PASSWORD = "' + password_ + '" where SERVICE = "' + service_ + '"'
        self.conn.execute(command)
        self.conn.commit()
        print("password updated successfully.")


    def delete_service(self,service_):
        command = 'DELETE from STORE where SERVICE = "' + service_ + '"'
        self.conn.execute(command)
        self.conn.commit()
        print("deleted from the database successfully.")


    def get_all(self, enc):
        self.cursor_.execute("SELECT * from STORE")
        data = self.cursor_.fetchall()
        if len(data) == 0:
            print('无数据')
        else:
            rows = []
            for row in data:
                rows.append([enc.decrypt(row[0]), enc.decrypt(row[1]), enc.decrypt(row[2])])
            self.output_service(rows)

    def output_service(self, rows):
        tb = pt.PrettyTable()
        tb.field_names = ["service", "username", "password"]
        for row in rows:
            tb.add_row([row[0], row[1], row[2]])
        print(tb)

    def is_service_present(self,service_):
        self.cursor_.execute("SELECT SERVICE from STORE where SERVICE = ?", (service_,))
        data = self.cursor_.fetchall()
        if len(data) == 0:
            print('没有匹配的服务')
            return False
        else:
            return True

    def close_db(self):
        self.conn.close()

    def store(self, enc):
        service = input("请输入服务名称：\n")
        service_enc = enc.encrypt(service)
        self.cursor_.execute("SELECT SERVICE from STORE where SERVICE = ?", (service_enc,))
        data = self.cursor_.fetchall()
        if len(data) == 0:
            username = input("输入 username : ")
            password = self.pwd_option()
            if username == '' or password == '':
                print("账号或密码为空")
            else:
                self.add_password(service_enc, enc.encrypt(username), enc.encrypt(password))
                rows = [[service, username, password]]
                self.output_service(rows)
                print("\n" + service.capitalize() + " 密码保存成功\n")

        else:
            print("服务 {} 已经存在".format(service))

    def get(self, enc):
        service = input("请输入服务名称：\n")
        service_enc = enc.encrypt(service)
        flag = self.is_service_present(service_enc)
        if flag:
            username, password = self.get_password(service_enc)
            rows = [[service, enc.decrypt(username), enc.decrypt(password)]]
            self.output_service(rows)

    def update(self, enc):
        service = input("请输入服务名称：\n")
        if service == '':
            print('服务名称为空！')
        else:
            service_enc = enc.encrypt(service)
            flag = self.is_service_present(service_enc)
            if flag:
                password = self.pwd_option()
                rows = [[service, ' ', password]]
                self.output_service(rows)
                self.update_password(service_enc, enc.encrypt(password))

    def delete(self, enc):
        service = input("请输入服务名称：\n")
        if service == '':
            print('服务名称为空！')
        else:
            service_enc = enc.encrypt(service)
            flag = self.is_service_present(service_enc)
            if flag:
                self.delete_service(service_enc)

    def pwd_option(self):
        print("密码选项：")
        print("0 输入密码")
        print("1 生成密码")
        option = input("请输入选项: ")
        password = ''
        if int(option) == 0:
            password = getpass("输入 password : ")
        else:
            pwd_length = input("请输入密码长度: ")
            password = pwd_generate(pwd_length)
        return password

    def batch_add_ip(self, enc):
        pwd_length = input("请输入密码长度: ")
        ip_list = []
        ip_file = 'ip_list.txt'
        with open(ip_file, "r") as f:
            ip_list = f.read().splitlines()
        rows = []
        for ip in ip_list:
            password = pwd_generate(pwd_length)
            rows.append([ip, 'root', password])
            self.add_password(enc.encrypt(ip), enc.encrypt('root'), enc.encrypt(password))
        self.output_service(rows)

    def batch_store(self, enc):
        pass_list = []
        pass_file = 'pass_list.txt'
        with open(pass_file, "r", encoding='UTF-8') as f:
            pass_list = f.read().splitlines()

        rows = []
        for pass_ in pass_list:
            pass_info = pass_.split(' ')
            rows.append(pass_info)
            self.add_password(enc.encrypt(pass_info[0]), enc.encrypt(pass_info[1]), enc.encrypt(pass_info[2]))
        self.output_service(rows)

    def vertify_admin(self, password):
        pwd_hash = hashlib.sha1(password.encode(encoding='UTF-8')).hexdigest()
        self.cursor_.execute("SELECT PASSWORD from administrator where PASSWORD = ?", (pwd_hash,))
        data = self.cursor_.fetchall()
        if len(data) == 0:
            return False
        else:
            return True

    def is_admin(self):
        self.cursor_.execute("SELECT PASSWORD from administrator")
        data = self.cursor_.fetchall()
        if len(data) == 0:
            return False
        else:
            return True

    def create_admin(self, password):
        pwd_hash = hashlib.sha1(password.encode(encoding='UTF-8')).hexdigest()
        command = 'INSERT INTO administrator(PASSWORD) VALUES("'+pwd_hash+'");'
        self.conn.execute(command)
        self.conn.commit()


