import psutil
from services.types import Attributes

# attr = option.get('attributes', None)

class ServiceNetwork:
	service_name = "network"

	def net_io_counters(service_key: str, **kwargs):
		attr: Attributes = kwargs['attr']
		pernic: bool = kwargs['params'].get('pernic')
		result = psutil.net_io_counters(pernic=pernic)
		if not pernic:
			result = { "global": result }

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{service_key}-{network_name}": getattr(snetio, attr_name, None)} for network_name, snetio in result.items()]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries

	def net_if_addrs(service_key: str, **kwargs):
		attr: Attributes = kwargs['attr']
		return []

	# Require root permissions on certain OS
	def net_connections(service_key: str, **kwargs):
		attr: Attributes = kwargs['attr']
		kind: str = kwargs['params'].get('kind')
		result = psutil.net_connections(kind=kind)

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{service_key}-{net_index}": getattr(result[net_index], attr_name, None)} for net_index in range(len(result))]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries

	def net_if_stats(service_key: str, **kwargs):
		attr: Attributes = kwargs['attr']
		result = psutil.net_if_stats()

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{service_key}-{snic_name}": getattr(snicstats, attr_name, None)} for snic_name, snicstats in result.items()]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries
