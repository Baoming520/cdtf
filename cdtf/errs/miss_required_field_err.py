#!python
# -*- coding: utf-8 -*-
'''
@File: miss_required_field_err.py
@Date: 2023/04/16 17:48:42
@Version: 1.0
@Description: None
'''

from just_logger import Logger, LogLevel

class MissRequiredFieldErr(Exception):
    def __init__(self, field_name: str):
        # Initialize a logger
        logger_name = 'cdtf'
        self.__logger = Logger(logger_name, level=LogLevel.ERROR)
        self.__logger.add_stream_handler(level=LogLevel.ERROR)
        self.__logger.add_file_handler(f'{logger_name}.log', level=LogLevel.ERROR)

        if field_name == 'id':
            self.msg = f"The 'id' column is very important to identify a test case."
        elif field_name == 'description':
            self.msg = f"The 'description' column is very important to record your verification content."
        elif field_name == 'verification':
            self.msg = f"The 'verification' column is very important to record you verification way."
        elif field_name == 'comments':
            self.msg = f"The 'comments' column is very important to record additional inforamtions."
        elif field_name == 'bugs':
            self.msg = f"The 'bugs' column is very important to record the bugs if have some."

        self.field_name = field_name
        self.__logger.log(f'{self.msg} (field_name={self.field_name})')
    

    def __str__(self):
        return f'{self.msg} (FieldName={self.field_name})'