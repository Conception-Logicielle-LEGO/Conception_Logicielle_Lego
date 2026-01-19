import sys
import logging

arguments = sys.argv
logging.basicConfig(filename=arguments[1], encoding='utf-8', level=logging.DEBUG)