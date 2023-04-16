#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@File: exceptions.py
@Date: 2022/05/12 18:42:48
@Version: 0.1.0
@Description: None
'''

from just_logger import Logger, LogLevel

class IllegalTemplateErr(Exception):
    def __init__(self, filename: str, msg: str=None):
        # Initialize a logger
        logger_name = 'cdtf'
        self.__logger = Logger(logger_name, level=LogLevel.ERROR)
        self.__logger.add_stream_handler(level=LogLevel.ERROR)
        self.__logger.add_file_handler(f'{logger_name}.log', level=LogLevel.ERROR)

        if msg is None:
            self.msg = f'The format of the template "{filename}" is wrong.'
        else:
            self.msg = msg
        self.filename = filename
        self.__logger.log(f'{self.msg} (FileName={self.filename})')
    

    def __str__(self):
        return f'{self.msg} (FileName={self.filename})'

