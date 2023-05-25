from env_loader import env_loader

class DATABASE:
	INFLUX = 'influx'
	PROMETHEUS = "prometheus"


class Settings():
	""" Utils settings using environements variables
	"""
	AGENT_NAME: str = env_loader["AGENT_NAME"]
	TSDB_NAME: str = env_loader["TSDB_NAME"]
	if TSDB_NAME == DATABASE.INFLUX:
		INFLUX_BUCKET: str = env_loader["INFLUX_BUCKET"]
		INFLUX_ORG: str = env_loader["INFLUX_ORG"]
		INFLUX_TOKEN: str = env_loader["INFLUX_TOKEN"]
		INFLUX_URL: str = env_loader["INFLUX_URL"]
	elif TSDB_NAME == DATABASE.PROMETHEUS:
		PROMETHEUS_BUCKET: str = env_loader["PROMETHEUS_BUCKET"]
 
settings = Settings()