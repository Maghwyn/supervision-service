import os
from env_config import settings, DATABASE
from influx_vitals import run_influx_vitals
from prometheus_vitals import run_prometheus_vitals
from sys import platform

if platform == "darwin":
	if os.getuid() != 0:
		raise Exception('In darwin environment, it is required to run as sudo due to some psutil.AccessDenied')

if not os.path.exists('logs.txt'):
	os.mknod('logs.txt')

if not os.path.exists('config.yaml'):
	os.mknod('config.yaml')
	raise Exception("config.yaml wasn't found, the file was created for you but you need to configure it")

# Open, clear, close
open('logs.txt', 'w').close()

if __name__ == '__main__':
	if settings.TSDB_NAME == DATABASE.INFLUX:
		run_influx_vitals()
	elif settings.TSDB_NAME == DATABASE.PROMETHEUS:
		run_prometheus_vitals()