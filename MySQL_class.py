#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 11:07:27 2022

@author: vladbad
"""

import pymysql


class MySQL:
    
    def __init__(self,host,user,password):
        self.host = host
        self.user = user
        self.password = password

    def __connect__(self):
        self.conn = pymysql.connect(host=self.host,user=self.user,
                        password=self.password,autocommit=True)
        self.cursor = self.conn.cursor()
    def __disconnect__(self):
        self.conn.close()
    
    def execute(self,sql):
        self.__connect__()
        self.cursor.execute(sql)
        self.__disconnect__()
    
    def fetch(self,sql):
        self.__connect__()
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.__disconnect__()
        
        row = [[item[0],item[1],item[2]] for item in result]
        return row
        