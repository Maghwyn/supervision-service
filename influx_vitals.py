import datetime
import yaml
import influxdb_client
import warnings
from env_config import settings, ENVIRONMENT
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

def influx_query_builder(queries, service_name: str, params):
	for query_index in range(len(queries)):
		point = influxdb_client.Point('system')
		point.tag("agent", settings.AGENT_NAME)
		point.tag(service_name, getattr(queries[query_index], 'tagValue'))
		# this breaks if we have more than 1 params
		if params is not None:
			for key, value in params.items():
				point.tag(key, value)

		for field in queries[query_index].get('fields'):
			for key, value in field.items():
				point.field(key, value)

		return point


def send_vitals(jobconfig):
	service_name = jobconfig.get('service_name')
	service_key = jobconfig.get('service_key')
	params = jobconfig.get('params')

	queries = jobconfig.get('service_method')(
		serviceKey=service_key,
		attr=jobconfig.get('attr'),
		params=params,
	)
	if not queries:
		warnings.warn(f"Returned queries was empty for service method {service_key}")
		return

	if settings.ENVIRONMENT == ENVIRONMENT.DEV:
		ts = datetime.datetime.now(datetime.timezone.utc)
		for query_index in range(len(queries)):
			logger.write('{0}: SERVICE {1} -> {2}\n'.format(ts.isoformat(), service_name, queries[query_index]))
	elif settings.ENVIRONMENT == ENVIRONMENT.PROD:
		record = influx_query_builder(queries=queries, service_name=service_name, params=params)
		write_api.write(bucket=settings.INFLUX_BUCKET, org=settings.INFLUX_ORG, record=record)


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
				jobconfig = {}
				jobconfig.update({ "service_method": getattr(service, method_name) })
				jobconfig.update({ "service_name": service_name })
				jobconfig.update({ "service_key": method_name })
				jobconfig.update({ "attr": method_config.get('attributes', None) })
				jobconfig.update({ "params": method_config.get('params', None) })
				interval = method_config.get('interval', 10)
				scheduler.add_job(send_vitals, 'interval', seconds=interval, args=[jobconfig], id=method_name)
			else:
				warnings.warn(f"Psutil ${method_name} function does not exist or is not supported, please verify the yaml configuration file")


def run_influx_vitals():
	scheduler = BlockingScheduler()
	register_job(scheduler)
	scheduler.start()
