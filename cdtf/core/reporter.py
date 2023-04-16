#!python
# -*- coding: utf-8 -*-
'''
@File: reporter.py
@Date: 2023/04/16 16:37:55
@Version: 0.1.0
@Description: None
'''

from datetime import datetime
from typing import Tuple
from cdtf.core.caseparser import CaseParser

import json
import os


class Reporter:
    _Passed = 'Passed'
    _Skipped = 'Skipped'
    _Failed = 'Failed'

    def __init__(self, stat_fi: str, xlsx_fi: str):
        self.reporttime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        self.testcases = CaseParser.parse(xlsx_fi)
        with open(stat_fi, mode='r', encoding='utf-8') as f:
            content = f.read()
        self.stat = json.loads(content)
        ...
    

    def aggregate(self) -> None:
        # Calculate coverage
        condition = {
            'verification': ('in', [ 'Adapter', 'Test Case', 'Unverified' ])
        }
        tcs = CaseParser.find(self.testcases, condition)
        cnt = 0
        for tc_nm in tcs:
            if tc_nm not in self.stat:
                continue

            results = self.stat[tc_nm]['results']
            passed_cnt, _, __ = self.__validate_results(results)
            if self.stat[tc_nm]['count'] > 0:
                cnt += 1
            else:
                print(tc_nm)
        
        self.coveredcases_cnt = cnt
        self.coverage = round(float(cnt) / float(len(tcs.keys())), 4)

        # Calculate pass rate
        condition = {
            'verification': ('in', [ 'Adapter', 'Test Case' ]),
            'comments': ('^ct', 'BUG#')
        }
        tcs = CaseParser.find(self.testcases, condition)
        self.inscopecases_cnt = len(tcs)
        self.case_statuses = {}
        self.case_status_cnt = {
            Reporter._Passed: 0,
            Reporter._Skipped: 0,
            Reporter._Failed: 0
        }
        cnt = 0
        for tc_nm in tcs:
            if tc_nm not in self.stat:
                continue
            
            results = self.stat[tc_nm]['results']
            passed_cnt, skipped_cnt, failed_cnt = self.__validate_results(results)
            if self.stat[tc_nm]['count'] > 0 and passed_cnt == len(results):
                cnt += 1
            
            status = 'Unknown'
            if passed_cnt > 0 and failed_cnt == 0:
                status = Reporter._Passed
            elif skipped_cnt == len(results):
                status = Reporter._Skipped
            elif failed_cnt > 0:
                status = Reporter._Failed
            self.case_statuses[tc_nm] = status
            self.case_status_cnt[status] += 1
            
        self.passrate = round(float(cnt) / float(len(tcs.keys())), 4)


    def report_as_raw(self):
        # Not implement now
        ...


    def report_as_xlsx(self):
        # Not implement now
        ...


    def report_as_html(self, title: str, bus_num: str, env_tag: str, out_dir: str) -> str:
        html = self.__load_html(dname='utils/data', fname='report_template.html')
        p_html, s_html, f_html = '', '', ''
        for id in self.case_statuses:            
            if self.case_statuses[id] == 'Passed':
                p_html += '<tr>'
                p_html += f"<td>{id}</td><td>{self.testcases[id].description}</td><td>Passed</td>"
                p_html += '</tr>'
            elif self.case_statuses[id] == 'Skipped':
                s_html += '<tr>'
                reason = '\n'.join(self.stat[id]['reason'])
                s_html += f"<td>{id}</td><td>{self.testcases[id].description}</td><td>Skipped</td><td>{reason}</td>"
                s_html += '</tr>'
            elif self.case_statuses[id] == 'Failed':
                f_html += '<tr>'
                f_html += f"<td>{id}</td><td>{self.testcases[id].description}</td><td>Failed</td>"
                f_html += '</tr>'
        
        html = html.replace('$REPORTTIME$', self.reporttime)
        html = html.replace('$TITLE$', title)
        html = html.replace('$BUSNUM$', bus_num)
        html = html.replace('$ENV$', env_tag)
        test_stat = f"{'/'.join(self.case_status_cnt.keys())}: {'/'.join([str(val) for val in self.case_status_cnt.values()])}"
        html = html.replace('$PASSNUM$', test_stat)
        html = html.replace('$INSCOPENUM$', str(self.inscopecases_cnt))
        html = html.replace('$AUTONUM$', str(self.coveredcases_cnt))
        html = html.replace('$PASSRATE$', str(self.passrate))
        html = html.replace('$COVERAGE$', str(self.coverage))
        html = html.replace('$PASSEDRECS$', p_html)
        html = html.replace('$SKIPPEDRECS$', s_html)
        html = html.replace('$FAILEDRECS$', f_html)
        report_name = datetime.strftime(datetime.now(), 'report_%Y%m%d%H%M%S.html')
        self.__save_html(out_dir, report_name, html)

        return os.path.join(out_dir, report_name)
    

    def report_as_text(self) -> str:
        report = {
            'inScopeCases': self.inscopecases_cnt,
            'coveredCases': self.coveredcases_cnt,
            'passrate': self.passrate,
            'coverage': self.coverage,
            'statistic': self.case_status_cnt,
            'caseStatus': self.case_statuses,
            'reportTime': self.reporttime
        }

        return json.dumps(report, indent=2, ensure_ascii=False)

    
    def __validate_results(self, results: list) -> Tuple[int, int, int]:
        passed_cnt, skipped_cnt, failed_cnt = 0, 0, 0
        for res in results:
            passed_cnt += int(res == Reporter._Passed)
            skipped_cnt += int(res == Reporter._Skipped)
            failed_cnt += int(res == Reporter._Failed)
        
        return passed_cnt, skipped_cnt, failed_cnt
    

    def __load_html(self, dname: str, fname: str) -> str:
        # add some specified process later
        fpath = os.path.join(os.getcwd(), dname, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content


    def __save_html(self, dname: str, fname: str, html: str) -> None:
        fpath = os.path.join(os.getcwd(), dname, fname)
        with open(fpath, 'w+', encoding='utf-8') as f:
            f.write(html)
