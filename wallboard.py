#!/usr/bin/env python

import os
import time

from ua import ua
from layout import layout
from system import system

system = system()

ua = ua()
configuration = ua.getConfig(system.getMacAddress())

layout = layout(configuration)

while True:
	records = []
	import pprint
	for queue in configuration['queues']:
		records.append(ua.getQueue(queue))
	layout.render(records)
	time.sleep(configuration['refresh_interval'])
