#_*_coding:utf-8_*_
__author__ = 'Alex Li'


import sys,os


if __name__ == "__main__":
    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(BASEDIR)
    from core import main
    main.CommandManagement(sys.argv)
