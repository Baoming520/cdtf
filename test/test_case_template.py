#!python
# -*- coding: utf-8 -*-
'''
@File: test_case_template.py
@Date: 2021/05/20 17:00:31
@Version: 0.1.0
@Description: None
'''

from cdtf.core import CaseParser
from just_logger import Logger, LogLevel

import unittest


class VerifyCaseTemplate(unittest.case.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger_name = 'test'
        cls.logger = Logger(logger_name, level=LogLevel.DEBUG)
        cls.logger.add_stream_handler(LogLevel.DEBUG)
        cls.logger.add_file_handler(f"{logger_name}.log", LogLevel.INFO)

        return super().setUpClass()


    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()
    

    def setUp(self) -> None:
        self.logger = VerifyCaseTemplate.logger

        return super().setUp()
    

    def tearDown(self) -> None:
        return super().tearDown()
    

    def test_case_template(self) -> None:
        field_infos = [
            { 'name': 'id', 'index': 0, 'required': True },
            { 'name': 'name', 'index': 1, 'required': False },
            { 'name': 'entry', 'index': 2, 'required': False },
            { 'name': 'description', 'index': 3, 'required': True },
            { 'name': 'verification', 'index': 4, 'required': True },
            { 'name': 'comments', 'index': 5, 'required': True }
        ]
        testcases = CaseParser.parse(xlsx_file='test/data/DemoTestCases.xlsx', case_row_index=11, field_infos=field_infos)
        print(testcases)

        condition = {
            'verification': ('in', [ 'Adapter', 'Test Case', 'Unverified' ])
        }
        filtered = CaseParser.find(testcases, condition)
        self.assertEquals(
            set(['DEMO_TC1','DEMO_TC2','DEMO_TC3','DEMO_TC4','DEMO_TC5','DEMO_TC6','DEMO_TC7','DEMO_TC8','DEMO_TC9','DEMO_TC10','DEMO_TC11','DEMO_TC12','DEMO_TC14']),
            set(filtered.keys())
        )


        condition = {
            'verification': ('in', [ 'Adapter', 'Test Case' ]),
            'comments': ('^ct', 'BUG#')
        }
        filtered = CaseParser.find(testcases, condition)
        self.assertEquals(
            set(['DEMO_TC2','DEMO_TC3','DEMO_TC4','DEMO_TC5','DEMO_TC6','DEMO_TC7','DEMO_TC8','DEMO_TC9','DEMO_TC10','DEMO_TC11','DEMO_TC12']),
            set(filtered.keys())
        )
        pass