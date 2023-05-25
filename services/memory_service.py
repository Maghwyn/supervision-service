import psutil
from services.types import Attributes

# attr = option.get('attributes', None)

class ServiceMemory:
	service_name = "memory"

	def virtual_memory(serviceKey: str, **kwargs):
		attr: Attributes = kwargs['attr']
		result = psutil.virtual_memory()
		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{serviceKey}-{memory_index}": getattr(result[memory_index], attr_name, None)} for memory_index in range(len(result))]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries

	def swap_memory(serviceKey: str, **kwargs):
		attr: Attributes = kwargs['attr']
		result = psutil.swap_memory()

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{serviceKey}-{memory_index}": getattr(result[memory_index], attr_name, None)} for memory_index in range(len(result))]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries