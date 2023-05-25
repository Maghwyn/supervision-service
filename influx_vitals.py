import time
import yaml
import influxdb_client
import warnings
from env_config import settings
from influxdb_client.client.write_api import SYNCHRONOUS
from apscheduler.schedulers.blocking import BlockingScheduler
from services.cpu_service import ServiceCPU
from services.disks_service import ServiceDisks
from services.memory_service import ServiceMemory
from services.network_service import ServiceNetwork

with open('config.yaml', 'r') as config_file:
	yamlConfig = yaml.load(config_file, Loader=yaml.FullLoader)

logger = open('logs.txt', 'a')
client = influxdb_client.InfluxDBClient(
	url=settings.INFLUX_URL,
	token=settings.INFLUX_TOKEN,
	org=settings.INFLUX_ORG
)
write_api = client.write_api(write_options=SYNCHRONOUS)

services = {
	ServiceCPU.service_name: ServiceCPU,
	ServiceDisks.service_name: ServiceDisks,
	ServiceMemory.service_name: ServiceMemory,
	ServiceNetwork.service_name: ServiceNetwork,
}

def register_job(scheduler):
	vitalsServices = yamlConfig.get('services', None)
	if vitalsServices is None:
		raise Exception('config.yaml services is not defined')

	for service_name, service_config in vitalsServices.items():
		service = services.get(service_name, None)

		if service is None:
			raise Exception(f'{service} does not exist as a service, please verify your yaml configuration')

		for method_name, method_config in service_config.items():
			if method_config.get('active') is not True:
				pass

			if hasattr(service, method_name):
				service_method = getattr(service, method_name)
				queries = service_method(
					serviceKey=method_name,
					attr=method_config.get('attributes', None),
					params=method_config.get('params', None),
				)

				if not queries:
					warnings.warn(f"Returned queries was empty for service name {service}")
					pass

				print(method_name, queries)
			else:
				warnings.warn(f"Psutil ${service} function does not exist or is not supported, please verify the yaml configuration file")


def run_influx_vitals():
	scheduler = BlockingScheduler()
	register_job(scheduler)
	scheduler.start()
