import psycopg2
from environs import Env
from psycopg2._psycopg import cursor
from psycopg2 import extras

env = Env()
env.read_env()


DBNAME = env('DBNAME')
DBUSER = env('DBUSER')
DBPASSWORD = env('DBPASSWORD')
DBHOST = env('DBHOST')
DBPORT = env('DBPORT')


class PostgresConnection:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, dbname, user, password, host, port):
        self.__dbname = dbname
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port

    def __connect_db(self, factory: str = None):
        connect = psycopg2.connect(
            dbname=self.__dbname,
            user=self.__user,
            password=self.__password,
            host=self.__host,
            port=self.__port
        )
        connect.autocommit = True

        if factory == 'dict':
            cur = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        elif factory == 'list':
            cur = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
        else:
            cur = connect.cursor()

        return cur

    @staticmethod
    def __execute(cur: cursor, query: str, data=None):
        if data:
            if isinstance(data, list):
                cur.executemany(query, data)
            else:
                cur.execute(query, data)
        else:
            cur.execute(query)

    @staticmethod
    def __fetch(cur: cursor, clean):
        if clean:
            fetch = cur.fetchone()[0]
        else:
            fetch = cur.fetchone()

        return fetch

    @staticmethod
    def __error(error):
        print(error)

    def fetch_one(self, query: str, data=None, factory=None, clean=False):
        try:
            with self.__connect_db(factory) as cur:
                self.__execute(cur, query, data)
                return self.__fetch(cur, clean)
        except (Exception, psycopg2.Error) as error:
            self.__error(error)

    def fetch_all(self, query: str, data=None, factory=None):
        try:
            with self.__connect_db(factory) as cur:
                self.__execute(cur, query, data)
                return cur.fetchall()
        except (Exception, psycopg2.Error) as error:
            self.__error(error)

    def update_query(self, query: str, data=None, message='OK'):
        try:
            with self.__connect_db() as cur:
                self.__execute(cur, query, data)
                print(message)
        except (Exception, psycopg2.Error) as error:
            self.__error(error)
