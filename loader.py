#!/usr/bin/python3
import os

config = os.path.join('.', 'config', 'config.py')
if os.path.isfile(config):
	try:
		from config.config import TOKEN
	except:
		raise Exception('Cannot find TOKEN variable, is it set?')
	try:
		from config.config import PREFIX
	except:
		raise Exception('Cannot find PREFIX variable, is it set?')
