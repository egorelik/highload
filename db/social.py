from mysql.connector import connect

class SocialDB:
    def init(self, config):
        self.config = config

    def connect(self):
        config = self.config
        try:
             self.connection = connect(host=config['MYSQL_HOST'], database=config['MYSQL_DB'], user=config['MYSQL_USER'],
                                      password=config['MYSQL_PASSWORD'], auth_plugin='mysql_native_password')
        except:
             print("MySQL connection error")

    def display_all_users(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user;")
        records = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return records;

    def add_new_user(self,user):
        self.connect()
        sql_stmt = """INSERT INTO user (username,password,first_name,last_name,age,city,country) 
                      VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cursor = self.connection.cursor(prepared=True)
        cursor.execute(sql_stmt, user)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def select_user(self,user):
        self.connect()
        sql_stmt = f"SELECT * FROM user WHERE username = %s"
        cursor = self.connection.cursor()
        cursor.execute(sql_stmt,(user,))
        records = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return records

    def search_user(self,query):
        self.connect()
        sql_stmt = f"SELECT * FROM user WHERE username LIKE '%{query}%' OR email LIKE '%{query}%'"
        cursor = self.connection.cursor()
        cursor.execute(sql_stmt)
        records = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return records

    def update_user(self,user):
        self.connect()
        sql_stmt = """UPDATE user SET updated_at = NOW(), username = %s,password = %s, first_name = %s, last_name = %s, 
                     age = %i, city = %s WHERE id = %s"""
        cursor = self.connection.cursor(prepared=True)
        cursor.execute(sql_stmt, user)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def delete_user(self,id):
        self.connect()
        sql_stmt = "DELETE FROM user WHERE id = %s"
        param = (id)
        cursor = self.connection.cursor(prepared=True)
        cursor.execute(sql_stmt, param)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def add_new_interest(self,interest):
        self.connect()
        sql_stmt = "INSERT INTO interest (interest) VALUES (%s)"
        cursor = self.connection.cursor(prepared=True)
        cursor.execute(sql_stmt, interest)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def select_interest(self,interest):
        self.connect()
        sql_stmt = f"SELECT * FROM interest WHERE username = %s"
        cursor = self.connection.cursor()
        cursor.execute(sql_stmt,interest)
        records = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return records

    def delete_interest(self,id):
        self.connect()
        sql_stmt = "DELETE FROM interest WHERE id = %s"
        param = (id)
        cursor = self.connection.cursor(prepared=True)
        cursor.execute(sql_stmt, param)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def add_user_interest(self,ids):
        self.connect()
        sql_stmt = "INSERT INTO user_interest (user_id,interest_id) VALUES (%s,%s)"
        cursor = self.connection.cursor(prepared=True)
        cursor.execute(sql_stmt, ids)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def select_user_interest(self,user_id):
        self.connect()
        print(user_id)
        sql_stmt = """SELECT i.id,i.interest FROM interest i,user_interest ui, user u
                       WHERE ui.user_id = %s and u.id = ui.user_id and i.id = ui.interest_id"""
        cursor = self.connection.cursor()
        cursor.execute(sql_stmt, user_id)
        records = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return records

    def select_interests(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM interest;")
        records = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return records;

