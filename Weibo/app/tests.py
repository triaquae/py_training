from django.test import TestCase

# Create your tests here.



# def func():
#     print(x)
#     x = 5
#
#
# func()

import sys
class dog(object):
    def __init__(self):
        print("dog...")


print(getattr(sys.modules[__name__], 'dog'))
