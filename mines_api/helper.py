#!/usr/bin/env python
#coding:utf8

"""
Author:       ottocho
Filename:     helper.py
Date:         2018-09-05 16:21
Description:
    helper functions that helps logic between view and model
"""

import json
import datetime

__all__ = [
    'get_new_result',
    'camelize',
    'json_dumps',
]

def get_new_result():
    '''
    default return structure for JSON Response
    `ret`: return value:
            0: correct
            >0: error code
    `value`: query data from the request
    `text`: warning or error message if necessary
    '''
    return {
        'ret': 1,
        'text': None,
        'value': None,
    }


def uncamelize(s):
    '''
    convert string from `CamelCase` to `lower_case_with_underscores`
    '''
    buff, l = '', []
    for ltr in s:
        if ltr.isupper():
            if buff:
                l.append(buff)
                buff = ''
        buff += ltr
    l.append(buff)
    return '_'.join(l).lower()

def _camelize(s):
    '''
    convert string from `lower_case_with_underscores` to `camelCase`
    '''
    result = []
    l = s.split('_')
    l = iter( t.lower() for t in l )
    result.append(next(l))
    for t in l:
        if t == '': result.append('')
        else:
            result.append(t[0].upper()+t[1:])
    return ''.join(result)

def camelize(o):
    '''
    convert object to `camelcase`
    '''
    if o is None:
        return None
    if isinstance(o, str):
        return _camelize(o)
    if isinstance(o, dict):
        # only convert dict key
        r = {}
        for k, v in o.items():
            r[_camelize(k)] = v
        return r
    if isinstance(o, (list, tuple)):
        return type(o)(_camelize(k) for k in o)
    return o

def json_dumps(o):
    '''
    json dump to string
    '''
    def default(o):
        if type(o) is datetime.date or type(o) is datetime.datetime:
            return o.isoformat()
    return json.dumps(
        o,
        sort_keys=True,
        indent=1,
        default=default
    )
