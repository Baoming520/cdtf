#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@File: capture.py
@Date: 2022/05/10 16:14:30
@Version: 0.1.0
@Description: None
'''

from typing import Any, Container, Iterable
from just_logger import Logger, LogLevel
from utils.singleton import Singleton

import json
import os
import re
import unittest


@Singleton
class Capture(unittest.TestCase):
    def __init__(self, name: str, testcases: list[dict], outdir: str, logger_name: str, log_level: LogLevel, smooth: bool, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        
        # Initialize a logger
        self.__logger = Logger(logger_name, level=log_level)
        self.__logger.add_stream_handler(level=log_level)
        self.__logger.add_file_handler(f'{logger_name}.log', level=log_level)

        # Constants
        self.__VALID_VERIFICATIONS = ['Adapter', 'Test Case']
        self.__BUG_MARKER_REGEX = 'BUG#\\d{14}'

        self.name = name
        self.testcases = testcases
        self.outdir = outdir
        self.smooth = smooth
        self.v_stat = {}
    

    def assert_in(self, member: Any, container: Iterable or Container, tc_id: str, tc_description: str=None):
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertIn(member, container, f'{tc_id}: {tc_description}')
        else:
            if member in container:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: {member} not in {list(container)}', LogLevel.ERROR)
        
        self.__stat(tc_id, tc_description, passed)
    

    def assert_not_in(self, member: Any, container: Iterable or Container, tc_id: str, tc_description: str=None):
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertNotIn(member, container, f'{tc_id}: {tc_description}')
        else:
            if member not in container:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: {member} in {list(container)}', LogLevel.ERROR)
        
        self.__stat(tc_id, tc_description, passed)

    
    def assert_true(self, val: bool, tc_id: str, tc_description: str=None):
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertTrue(val, f'{tc_id}: {tc_description}')
        else:
            if val:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: Should be True but {val}', LogLevel.ERROR)
        
        self.__stat(tc_id, tc_description, passed)
    

    def assert_false(self, val: bool, tc_id: str, tc_description: str=None):
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertFalse(val, f'{tc_id}: {tc_description}')
        else:
            if not val:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: Should be False but {val}', LogLevel.ERROR)
        
        self.__stat(tc_id, tc_description, passed)

    
    def assert_is(self, exp_val: Any, act_val: Any, tc_id: str, tc_description: str=None) -> None:
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertIs(exp_val, act_val, f'{tc_id}: {tc_description}')
        else:
            if act_val is exp_val:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: Expected={exp_val}, Actual={act_val}', LogLevel.ERROR)
        
        self.__stat(tc_id, tc_description, passed)


    def assert_is_not(self, exp_val: Any, act_val: Any, tc_id: str, tc_description: str=None) -> None:
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertIsNot(exp_val, act_val, f'{tc_id}: {tc_description}')
        else:
            if act_val is not exp_val:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: Expected={exp_val}, Actual={act_val}', LogLevel.ERROR)
        
        self.__stat(tc_id, tc_description, passed)


    def assert_equal(self, exp_val: Any, act_val: Any, tc_id: str, tc_description: str=None) -> None:
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertEqual(exp_val, act_val, f'{tc_id}: {tc_description}')
        else:
            if exp_val == act_val:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: Expected={exp_val}, Actual={act_val}', LogLevel.ERROR)
                
        self.__stat(tc_id, tc_description, passed)
    
    
    def assert_not_equal(self, exp_val: Any, act_val: Any, tc_id: str, tc_description: str=None) -> None:
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertNotEqual(exp_val, act_val, f'{tc_id}: {tc_description}')
        else:
            if exp_val != act_val:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: Expected={exp_val}, Actual={act_val} (They are should not be equal with each others.)', LogLevel.ERROR)
                
        self.__stat(tc_id, tc_description, passed)
    

    def assert_greater(self, val1: Any, val2: Any, tc_id: str, tc_description: str=None) -> None:
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertGreater(val1, val2, f'{tc_id}: {tc_description}')
        else:
            if val1 > val2:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: Expected={val1}, Actual={val2}', LogLevel.ERROR)
                
        self.__stat(tc_id, tc_description, passed)


    def assert_greater_equal(self, val1: Any, val2: Any, tc_id: str, tc_description: str=None) -> None:
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertGreaterEqual(val1, val2, f'{tc_id}: {tc_description}')
        else:
            if val1 >= val2:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: Expected={val1}, Actual={val2}', LogLevel.ERROR)
                
        self.__stat(tc_id, tc_description, passed)
    

    def assert_less(self, val1: Any, val2: Any, tc_id: str, tc_description: str=None) -> None:
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertLess(val1, val2, f'{tc_id}: {tc_description}')
        else:
            if val1 < val2:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: Expected={val1}, Actual={val2}', LogLevel.ERROR)
                
        self.__stat(tc_id, tc_description, passed)
    

    def assert_less_equal(self, val1: Any, val2: Any, tc_id: str, tc_description: str=None) -> None:
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            self.assertLessEqual(val1, val2, f'{tc_id}: {tc_description}')
        else:
            if val1 <= val2:
                passed = True
                self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
            else:
                passed = False
                self.__logger.log(f'FAILED - {tc_id} - {tc_description}', LogLevel.ERROR)
                self.__logger.log(f'Assert Error: Expected={val1}, Actual={val2}', LogLevel.ERROR)
                
        self.__stat(tc_id, tc_description, passed)
    

    def assert_direct(self, tc_id: str, tc_description: str=None) -> None:
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            return
        else:
            passed = True
            self.__logger.log(f'PASSED - {tc_id} - {tc_description}', LogLevel.INFO)
                 
        self.__stat(tc_id, tc_description, passed)
    

    def skip(self, tc_id: str, tc_description: str=None) -> None:
        v_flag = self.__validate(tc_id, tc_description)
        if not v_flag:
            return

        if not self.smooth:
            return
        else:
            self.__logger.log(f'SKIPPED - {tc_id} - {tc_description}', LogLevel.WARNING)
        
        self.__stat(tc_id, tc_description, None, 'Skip the current test case actively.')

    
    def save_stat(self, raw_fname: str) -> None:
        outfile = os.path.join(self.outdir, raw_fname)
        with open(outfile, 'w+', encoding='utf-8') as f:
            content = json.dumps(self.v_stat, ensure_ascii=False)
            f.write(content)
    

    def __validate(self, tc_id: str, tc_description: str):
        w_flag = False
        if not w_flag and tc_id not in self.testcases.keys():
            w_flag = True
            msg = f'The id is not found in the test case specification, please add it before testing.'
        if not w_flag and self.testcases[tc_id].verification not in self.__VALID_VERIFICATIONS:
            w_flag = True
            msg = f'Please update the value of verification to "Adapter" or "Test Case" before testing.'
        
        if not w_flag:
            bugs = re.findall(self.__BUG_MARKER_REGEX, self.testcases[tc_id].comments) 
            if bugs is not None and len(bugs) > 0:
                w_flag = True
                msg = f'Bugs {bugs} found, please fix them first and then remove the bug id from comments before testing.'

        if w_flag:
            self.__logger.log(f'SKIPPED - {tc_id} - {tc_description}', LogLevel.WARNING)
            self.__logger.log(msg, LogLevel.WARNING)
            self.__stat(tc_id, tc_description, passed=None, reason=msg) 

            return False
        
        return True


    def __stat(self, tc_id: str, tc_description: str, passed: bool or None, reason: str=None):
        result = 'Skipped' if passed is None else ('Passed' if passed else 'Failed') 
        if tc_id not in self.v_stat:
            self.v_stat[tc_id] = {}
            self.v_stat[tc_id]['count'] = 1
            self.v_stat[tc_id]['results'] = [ result ]
            if result == 'Skipped':
                self.v_stat[tc_id]['reason'] = [ reason ]
        else:
            self.v_stat[tc_id]['count'] += 1
            self.v_stat[tc_id]['results'].append(result)
            if result == 'Skipped':
                self.v_stat[tc_id]['reason'].append(reason)
        
        if 'description' not in self.v_stat[tc_id]:
            self.v_stat[tc_id]['description'] = tc_description