#_*_coding:utf-8_*_
__author__ = 'Alex Li'


import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stark.settings")

    from Stark import house_management

    house_manager = house_management.HouseManager(sys.argv)
    house_manager.argv_parse_and_invoke()
