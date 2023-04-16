#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@File: singleton.py
@Date: 2022/05/10 16:26:43
@Version: 0.1.0
@Description: None
'''

def singleton_n(cls):
    instance = {}

    def get_instance(*args, **kwargs):
        instance = cls(*args, **kwargs)
        if cls not in instance:
            instance[cls] = instance

        return instance[cls]
    
    return get_instance


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        instance = cls(*args, **kwargs)
        if hasattr(instance, 'name') and instance.name not in instances:
            instances[instance.name] = instance
            
        return instances[instance.name]
    
    return get_instance



class Singleton_N(object):
    def __init__(self, cls):
        self.__cls = cls
        self.__instance = {}
    

    def __call__(self, *args, **kwargs):
        if self.__cls not in self.__instance:
            self.__instance[self.__cls] = self.__cls(*args, **kwargs)

        return self.__instance[self.__cls]


class Singleton(object):
    def __init__(self, cls):
        self.__cls = cls
        self.__instances = {}
    

    def __call__(self, *args, **kwargs):
        instance = self.__cls(*args, **kwargs)
        if hasattr(instance, 'name') and instance.name not in self.__instances:
            self.__instances[instance.name] = instance

        return self.__instances[instance.name]