import psutil
from services.types import Attributes


# attr = option.get('attributes', None)

class ServiceCPU:
	service_name = "cpu"

	def cpu_times(service_key: str, **kwargs):
		attr: Attributes = kwargs['attr']
		percpu: bool = kwargs['params'].get('percpu')
		result = psutil.cpu_times(percpu=percpu)
		if not percpu:
			result = [result]

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{service_key}-{cpu_index}": getattr(result[cpu_index], attr_name, None)} for cpu_index in range(len(result))]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries

	def cpu_percent(service_key: str, **kwargs):
		percpu: bool = kwargs['params'].get('percpu')
		result = psutil.cpu_percent(percpu=percpu)
		if not percpu:
			result = [result]

		queries = []
		if all(element == 0.0 for element in result) or all(element == None for element in result):
			return queries

		fields = [{f"{service_key}-{cpu_index}": result[cpu_index]} for cpu_index in range(len(result))]
		queries.append({ "tagValue": "percent", "fields": fields })
		return queries

	def cpu_times_percent(service_key: str, **kwargs):
		attr: Attributes = kwargs['attr']
		percpu: bool = kwargs['params'].get('percpu')
		result = psutil.cpu_times_percent(percpu=percpu)
		if not percpu:
			result = [result]

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{service_key}-{cpu_index}": getattr(result[cpu_index], attr_name, None)} for cpu_index in range(len(result))]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries

	def cpu_stats(service_key: str, **kwargs):
		attr: Attributes = kwargs['attr']
		result = [psutil.cpu_stats()]

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{service_key}-{cpu_index}": getattr(result[cpu_index], attr_name, None)} for cpu_index in range(len(result))]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries
