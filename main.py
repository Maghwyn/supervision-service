import os
from env_config import settings, DATABASE
from influx_vitals import run_influx_vitals
from prometheus_vitals import run_prometheus_vitals

if not os.path.exists('logx.txt'):
	os.mknod('logs.txt')

if not os.path.exists('config.yaml'):
	os.mknod('config.yaml')
	raise Exception("config.yaml wasn't found, the file was created for you but you need to configure it")

# Open, clear, close
open('log.txt', 'w').close()

if __name__ == '__main__':
	if settings.TSDB_NAME == DATABASE.INFLUX:
		run_influx_vitals()
	elif settings.TSDB_NAME == DATABASE.PROMETHEUS:
		run_prometheus_vitals()