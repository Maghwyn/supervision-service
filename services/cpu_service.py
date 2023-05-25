import psutil
from services.types import Attributes


# attr = option.get('attributes', None)

class ServiceCPU:
	service_name = "cpu"

	def cpu_times(serviceKey: str, attr: Attributes, percpu = False):
		result = psutil.cpu_times(percpu=percpu)
		if not percpu:
			result = [result]

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{serviceKey}-{cpu_index}": result[cpu_index][attr_name]} for cpu_index in range(len(result))]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries

	def cpu_percent(serviceKey: str, percpu = False):
		result = psutil.cpu_percent(percpu=percpu)
		if not percpu:
			result = [result]

		queries = []
		if all(result) == 0.0 or all(result) == None:
			return queries
  
		fields = [{f"{serviceKey}-{cpu_index}": result[cpu_index]} for cpu_index in range(len(result))]
		queries.append({ "tagValue": "percent", "fields": fields })
		return queries

	def cpu_times_percent(serviceKey: str, attr: Attributes, percpu = False):
		result = psutil.cpu_times_percent(percpu=percpu)
		if not percpu:
			result = [result]

		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{serviceKey}-{cpu_index}": result[cpu_index][attr_name]} for cpu_index in range(len(result))]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries

	def cpu_stats(serviceKey: str, attr: Attributes):
		result = [psutil.cpu_stats()]
  
		queries = []
		for attr_name, active in attr.items():
			if not active:
				pass

			fields = [{f"{serviceKey}-{cpu_index}": result[cpu_index][attr_name]} for cpu_index in range(len(result))]
			queries.append({ "tagValue": attr_name, "fields": fields })

		return queries
