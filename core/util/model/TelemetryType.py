from enum import Enum

class TelemetryType(Enum):
	TEMPERATURE = 'temperature'
	PRESSURE = 'pressure'
	HUMIDITY = 'humidity'
	LIGHT = 'light'
	GAS = 'gas'
	AIR_QUALITY = 'airQuality'
	UV_INDEX = 'uvIndex'
	NOISE = 'noise'
	CO2 = 'co2'
	RAIN = 'rain'
	SUM_RAIN_1 = 'sum_rain_1'
	SUM_RAIN_24 = 'sum_rain_24'
	WIND_STRENGTH = 'wind_strength'
	WIND_ANGLE = 'wind_angle'
	GUST_STRENGTH = 'gust_strength'
	GUST_ANGLE = 'gust_angle'
