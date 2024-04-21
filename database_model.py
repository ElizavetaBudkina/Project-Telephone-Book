import psycopg2


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addClient(self, fam, name, ot, number, note):
        try:
            self.__cur.execute(f"INSERT INTO telbook (Fam, Im, Ot, tel, textnote) VALUES ('{fam}','{name}','{ot}','{number}','{note}');")
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка добавления клиента в БД " + str(e))
            return False
        return True

    def showClient(self):
        try:
            self.__cur.execute(f"SELECT * FROM telbook order by id;")
            res = self.__cur.fetchall()
            if res:
                return res
        except psycopg2.Error as e:
            print("Ошибка получения клиента из БД " + str(e))
        return False

