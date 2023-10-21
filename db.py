#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error
import logging
import logging.handlers
from sys import exit as sexit

from logger import logger
from other import isInt

def getLog(s, text):
    return f"db.py : [{s}] {text}"

class BD(object): # conn.rollback() откатывает до предыдущего conn.commit()
    def __init__(self, path):
        self.path = path
        self.conn = self.create_connection(path)
        self.cur = self.conn.cursor()

        if not self.table_exists("users"):
            if self.create_table_users() == 0:
                logger.info(getLog('+', "Table 'users' was created"))
            else:
                logger.critical(getLog('-', "Error! Table 'users' wasn't created"))
        else:
            logger.info(getLog('+', "Table 'users' was detected"))

        if not self.table_exists("stickers"):
            if self.create_table_stikers() == 0:
                logger.info(getLog('+', "Table 'stickers' was created"))
            else:
                logger.critical(getLog('-', "Error! Table 'stickers' wasn't created"))
        else:
            logger.info(getLog('+', "Table 'stickers' was detected"))

        if not self.table_exists("spheres"):
            if self.create_table_spheres() == 0:
                logger.info(getLog('+', "Table 'spheres' was created"))
            else:
                logger.critical(getLog('-', "Error! Table 'spheres' wasn't created"))
        else:
            logger.info(getLog('+', "Table 'spheres' was detected"))

        if not self.table_exists("peoples"):
            if self.create_table_peoples() == 0:
                logger.info(getLog('+', "Table 'peoples' was created"))
            else:
                logger.critical(getLog('-', "Error! Table 'peoples' wasn't created"))
        else:
            logger.info(getLog('+', "Table 'peoples' was detected"))

    def __del__(self):
        self.conn.close()
        logger.info(getLog('+', f"BD with path '{self.path}' (SQLite) was closed"))

    # Peoples

    def create_table_peoples(self): # Создаёт таблицу spheres
        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS peoples(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               phone TEXT,
               email TEXT);
            """)
            self.conn.commit()
            return 0
        except sqlite3.OperationalError as e:
            logger.error(getLog('-', f"Error in BD.create_table_peoples(...): {e}"))
            return None

    def append_peoples_item(self, item): # Добавляет name в spheres
        try:
            if not self.isTwinNameSpheres(item[0]):
                self.cur.execute(f"INSERT INTO peoples(name, number, email) VALUES(?, ?, ?);", item)
                self.conn.commit()
                return 0
            else:
                logger.info(getLog('?', f"Impossible to append item in spheres: name {item[0]} will be Twin!"))
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.append_spheres_item(...): {e}"))
        return None

    def get_all_peoples(self):
        try:
            self.cur.execute(f"SELECT name, phone, email FROM peoples;")
            result = self.cur.fetchall()
            return result
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.isTwinNamePeoples(...): {e}"))
        return None

    def isTwinNamePeoples(self, name):
        try:
            self.cur.execute(f"SELECT * FROM peoples WHERE name=?;", (name,))
            result = self.cur.fetchall()
            if len(result) > 0:
                return True
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.isTwinNamePeoples(...): {e}"))
        return False

    # Spheres

    def create_table_spheres(self): # Создаёт таблицу spheres
        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS spheres(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT);
            """)
            self.conn.commit()
            return 0
        except sqlite3.OperationalError as e:
            logger.error(getLog('-', f"Error in BD.create_table_spheres(...): {e}"))
            return None

    def append_spheres_item(self, name): # Добавляет name в spheres
        try:
            if not self.isTwinNameSpheres(name):
                self.cur.execute(f"INSERT INTO spheres(name) VALUES(?);", name)
                self.conn.commit()
                return 0
            else:
                logger.info(getLog('?', f"Impossible to append item in spheres: name {name} will be Twin!"))
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.append_spheres_item(...): {e}"))
        return None

    def isTwinNameSpheres(self, name):
        try:
            self.cur.execute(f"SELECT * FROM spheres WHERE name=?;", (name,))
            result = self.cur.fetchall()
            if len(result) > 0:
                return True
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.isTwinNameSpheres(...): {e}"))
        return False

    # Users

    def create_table_users(self): # Создаёт таблицу users
        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
               id INT PRIMARY KEY,
               username TEXT,
               area TEXT,
               kitchen TEXT,
               part TEXT,
               admin BOOLEAN);
            """)
            self.conn.commit()
            return 0
        except sqlite3.OperationalError as e:
            logger.error(getLog('-', f"Error in BD.create_table_users(...): {e}"))
        return None

    def append_users_item(self, user): # Добавляет в users user
        try:
            if not self.isTwinId("users", user[0]):
                self.cur.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?);", user)
                self.conn.commit()
                return 0
            else:
                logger.info(getLog('?', f"Impossible to append item in users: id {user[0]} will be Twin!"))
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.append_users_item(...): {e}"))
        return None

    def isAdminById(self, id):
        try:
            self.cur.execute(f"SELECT admin FROM users WHERE id=?;", (id,))
            result = self.cur.fetchall()
            if len(result) > 0:
                if result[0]:
                    return True
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.isAdminById(...): {e}"))
        return False

    # Stickers

    def create_table_stikers(self): # Создаёт таблицу stickers
        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS stickers(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               telegram_id TEXT,
               name TEXT,
               family TEXT);
            """)
            self.conn.commit()
            return 0
        except sqlite3.OperationalError as e:
            logger.error(getLog('-', f"Error in BD.create_table_stickers(...): {e}"))
            return None

    def append_stickers_item(self, sticker): # Добавляет sticker в stickers
        try:
            if not self.isTwinTelegramId(sticker[0]):
                self.cur.execute(f"INSERT INTO stickers(telegram_id, name, family) VALUES(?, ?, ?);", sticker)
                self.conn.commit()
                return 0
            else:
                logger.info(getLog('?', f"Impossible to append item in stickers: telegram_id {sticker[0]} will be Twin!"))
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.append_stickers_item(...): {e}"))
        return None

    def isTwinTelegramId(self, id):
        try:
            self.cur.execute(f"SELECT * FROM stickers WHERE telegram_id=?;", (id,))
            result = self.cur.fetchall()
            if len(result) > 0:
                return True
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.isTwinTelegramId(...): {e}"))
        return False

    #  Универсальные

    def table_exists(self, table): # Проверяет, существует ли table
        try:
            self.cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table}';")
            if len(self.cur.fetchall()) > 0:
                return True
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.table_exists(...): {e}"))
        return False

    def isTwinId(self, table, id):
        try:
            self.cur.execute(f"SELECT * FROM {table} WHERE id=?;", (id,))
            result = self.cur.fetchall()
            if len(result) > 0:
                return True
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.isTwinId(...): {e}"))
        return False

    def create_connection(self, path): # Соеджинение с бд (если не существует, то создаст новую по указанному пути)
        conn = None
        try:
            conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
            sqlite3.register_adapter(bool, int)
            sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
            logger.info(getLog('+', f"Connecting to DB '{path}' (SQLite) successfuly"))
        except Error as e:
            logger.critical(getLog('-', f"Error in BD.create_connection(...): {e}"))
            self.__del__()
            sexit(1)

        return conn

    def update_column_by_id(self, column, table, newStringValue, id): # Меняет в table по id значение column на newStringValue
        if isInt(id):
            try:
                self.cur.execute(
                    f"UPDATE {table} SET {column} = ? WHERE id = ?",
                    (newStringValue, id)
                )
                self.conn.commit()
                return 0
            except sqlite3.OperationalError as e:
                logger.warning(getLog('-', f"Error in BD.update_column_by_id(...): {e}"))
                return None
        else:
            return None

    def get_all(self, table): # Возвращяет все из table
        try:
            self.cur.execute(f"SELECT * FROM {table};")
            return self.cur.fetchall()
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.get_all(...): {e}"))
            return None

    def get_column_by_id(self, column, table, id): # Возвращяет знвчение column из table по id
        if isInt(id):
            one_result = None
            try:
                self.cur.execute(f"SELECT {column} FROM {table} WHERE id=?;", (id,))
                one_result = self.cur.fetchone()
                if one_result:
                    return one_result[0]
            except sqlite3.OperationalError as e:
                logger.warning(getLog('-', f"Error in BD.get_column_by_id(...): {e}"))
        return None

    def delete_item_by_id(self, table, id): # Удаляет элемент из table по id
        if isInt(id):
            try:
                self.cur.execute(f"DELETE FROM {table} WHERE id=?;", (id,))
                self.conn.commit()
                return 0
            except sqlite3.OperationalError as e:
                logger.warning(getLog('-', f"Error in BD.delete_item_by_id(...): {e}"))
                return None
        else:
            return None

    def delete_item_by_name(self, table, name): # Удаляет элемент из table по name
        try:
            self.cur.execute(f"DELETE FROM {table} WHERE name='?';", (name,))
            self.conn.commit()
            return 0
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.delete_item_by_name(...): {e}"))
        return None

    def rename_column(self, table, old_column, new_column): # В table переименовывает old_column на new_column
        try:
            self.cur.execute(f"ALTER TABLE {table} RENAME COLUMN {old_column} TO {new_column};")
            self.conn.commit()
            return 0
        except sqlite3.OperationalError as e:
            logger.warning(getLog('-', f"Error in BD.rename_column(...): {e}"))
            return None

#if __name__ == "__main__":
 #   logger.info("<-START->")

  #  bd = BD(BD_PATH)
  #  bd.append_users_item((123, 'NAME1', 'AREA1', 'KITCHEN1', 'PART1', False))
  #  bd.append_users_item((1234, 'NAME2', 'AREA2', 'KITCHEN2', 'PART2', True))
  #  bd.append_users_item((12345, 'NAME3', 'AREA3', 'KITCHEN3', 'PART3', True))
  #  bd.append_stickers_item(('qwe123', 'name', 'family'))
  #  bd.delete_item_by_id("users", 12345)
  #  bd.update_column_by_id("name", "users", "newName", 1234)
  #  bd.get_column_by_id("name", "users", 1234)
  #  print(bd.get_all("users"))
  #  print(bd.get_all("stickers"))
  #  del bd
  #  logger.info("<-SHUTDOWN->")