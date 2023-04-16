#!python
# -*- coding: utf-8 -*-
'''
@File: testcase.py
@Date: 2023/04/16 16:39:22
@Version: 0.1.0
@Description: None
'''

from datetime import datetime
from cdtf.errs import IllegalTemplateErr, MissRequiredFieldErr
from xml.dom import NotSupportedErr

import os
import xlrd

class CaseParser:
    @classmethod
    def _verify_field_infos(cls, field_infos: list):
        field_names = [fi['name'] for fi in field_infos]
        if 'id' not in field_names:
            raise MissRequiredFieldErr('id')
        if 'description' not in field_names:
            raise MissRequiredFieldErr('description')
        if 'verification' not in field_names:
            raise MissRequiredFieldErr('verification')
        if 'comments' not in field_names:
            raise MissRequiredFieldErr('comments')
        # if 'bugs' not in field_names:
        #     raise MissRequiredFieldErr('bugs')


    @classmethod
    def _verify_template(cls, cell, ncols):
        if len(cls._field_infos) != ncols:
            raise IllegalTemplateErr(filename=cls._xlsx_fname, msg=f"The count of fields is not follow the specification.")
        for fi_info in cls._field_infos:
            fi_name = fi_info['name']
            if cell(cls._case_row_idx, fi_info['index']).value != fi_name:
                raise IllegalTemplateErr(filename=cls._xlsx_fname, msg=f"The field '{fi_name}' is not matched with specification.")
     

    @classmethod
    def parse(cls, xlsx_file: str, case_row_index: int, field_infos: list, sheet_name: str='TestCases') -> dict:
        cls._case_row_idx = case_row_index
        cls._verify_field_infos(field_infos)
        cls._field_infos = field_infos
        cls._valid_field_names = [fi_info['name'] for fi_info in field_infos]
        cls._xlsx_fname = xlsx_file.replace(os.path.dirname(xlsx_file) + '\\', '')
        wb = xlrd.open_workbook(xlsx_file)
        t_sheet = wb.sheet_by_name(sheet_name)
        nrows = t_sheet.nrows
        ncols = t_sheet.ncols
        testcases = {}
        for i in range(0, nrows):
            if i < cls._case_row_idx:
                continue
            if i == cls._case_row_idx:
                cls._verify_template(t_sheet.cell, ncols)
                continue
            tc = {}
            for fi_info in cls._field_infos:
                c_idx, k = fi_info['index'], fi_info['name']
                tc[k] = t_sheet.cell(i, c_idx).value

            testcases[tc['id']] = tc

        return testcases
    
    @classmethod
    def find(cls, testcases: dict, cond: dict) -> dict:
        res = {}
        for tc_id in testcases:
            fit = True
            for kw in cond:
                if kw not in cls._valid_field_names:
                    continue
                optr, val = cond[kw]
                if optr == 'in':
                    fit = testcases[tc_id][kw] in val
                elif optr == '^in':
                    fit = testcases[tc_id][kw] not in val
                elif optr == 'eq':
                    fit = testcases[tc_id][kw] == val
                elif optr == '^eq':
                    fit = testcases[tc_id][kw] != val
                elif optr == 'ct':
                    fit = testcases[tc_id][kw].find(val) != -1
                elif optr == '^ct':
                    fit = testcases[tc_id][kw].find(val) == -1
                else:
                    raise NotSupportedErr(f'The operator {optr} is not supported.')
                
                if not fit:
                    break
            
            if fit:
                res[tc_id] = testcases[tc_id]
        
        return res