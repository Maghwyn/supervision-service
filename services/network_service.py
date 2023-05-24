import psutil
from services.types import Attributes

# attr = option.get('attributes', None)

class ServiceNetwork:
	service_name = "network"

	def net_io_counters(serviceKey: str, attr: Attributes, pernic = False):
		result = psutil.net_io_counters(pernic=pernic)
		if not pernic:
			result = { "global": result }

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{serviceKey}-{network_name}": snetio[attr_name]} for network_name, snetio in result.items()]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries

	def net_if_addrs(serviceKey: str, attr: Attributes):
		return []

	def net_connections(serviceKey: str, attr: Attributes, kind = 'inet'):
		result = psutil.net_connections(kind=kind)

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{serviceKey}-{memory_index}": result[memory_index][attr_name]} for memory_index in range(len(result))]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries

	def net_if_stats(serviceKey: str, attr: Attributes):
		result = psutil.net_if_stats()

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{serviceKey}-{disk_name}": diskio[attr_name]} for disk_name, diskio in result.items()]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries
