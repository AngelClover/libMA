#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2013-08-31 19:50:02

import time
import sqlite3
import basedb

class AccountDB(basedb.BaseDB):
    __tablename__ = 'account'
    def __init__(self, path='account.db'):
        self.conn = sqlite3.connect(path)
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS `%s` (
                id PRIMARY KEY,
                uid, pwd, name, lv, status, target_lv, rounds, intime, nextime, friends, friend_max
                )'''
                % self.__tablename__)
        self.conn.commit()

        # fix error
        for each in self.scan('RUNNING'):
            self.update(each['id'], status='PENDING')

    @property
    def dbcur(self):
        return self.conn.cursor()

    def add(self, _id, pwd, status='PENDING', target_lv=25):
        self._replace(self.__tablename__,
                id = _id,
                uid = 0,
                pwd = pwd,
                lv = 0,
                status = status,
                target_lv = target_lv,
                rounds = 0,
                intime = time.time(),
                friends = 20,
                friend_max = 20,
                nextime = 0)
        self.conn.commit()

    def scan(self, status):
        return self._select2dic(self.__tablename__,
                where="status='%s'" % status)

    def find_friends(self):
        return self._select2dic(self.__tablename__,
                where="friend_max - friends > 0")

    def get(self, _id):
        ret = self._select2dic(self.__tablename__,
                where="id='%d'" % int(_id), limit=1)
        if ret:
            return ret[0]
        else:
            return None

    def update(self, id=None, **data):
        if not id:
            id = data['id']
        self._update(self.__tablename__, "id='%d'" % int(id), **data)
        self.conn.commit()

class BattleDB(basedb.BaseDB):
    __tablename__ = 'battle'
    def __init__(self, path='battle.db'):
        self.conn = sqlite3.connect(path)
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS `%s` (
                uid INTEGER PRIMARY KEY,
                name, hp, atk, deck_rank
                )'''
                % self.__tablename__)
    @property
    def dbcur(self):
        return self.conn.cursor()

    def add(self, _id, hp=999999, atk=999999, deck_rank=100):
        self._replace(self.__tablename__, uid=int(_id), hp=hp, atk=atk, deck_rank=deck_rank)
        self.conn.commit()

    def update(self, id, hp, atk):
        self._update(self.__tablename__, "uid=%d" % int(id), hp=hp, atk=atk)
        self.conn.commit()

    def scan(self):
        return self._select2dic(self.__tablename__)

accountdb = AccountDB()
battledb = BattleDB()
