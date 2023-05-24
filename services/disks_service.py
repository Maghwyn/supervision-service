import re
import psutil
from services.types import Attributes

# attr = option.get('attributes', None)

class ServiceDisks:
	service_name = "disks"
	pattern = r"[\\/]?dev[\\/](.+)"

	def disk_usage(serviceKey: str, attr: Attributes):
		result = psutil.disk_partitions()

		queries = []
		diskParts = {}
		for part in result:
			usage = psutil.disk_usage(part.mountpoint)
			match = re.search(ServiceDisks.pattern, part.device)
			if match:
				diskParts.update({ f"{match.group(1)}": usage })
			else:
				pass

		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{serviceKey}-{disk_name}": diskusage[attr_name]} for disk_name, diskusage in diskParts.items()]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries

	def disk_io_counters(serviceKey: str, attr: Attributes, perdisk = False):
		result = psutil.disk_io_counters(perdisk=perdisk, nowrap=True)
		if not perdisk:
			result = { "global": result }

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{serviceKey}-{disk_name}": diskio[attr_name]} for disk_name, diskio in result.items()]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries