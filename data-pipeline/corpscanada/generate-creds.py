#!/usr/bin/python
import psycopg2
import datetime
from corpscanada.config import config
from corpscanada.eventprocessor import EventProcessor
from corpscanada.corporationscanada import CorporationsCanada, system_type
from corpscanada.eventprocessor import EventProcessor
from corpscanada.rocketchat_hooks import log_error, log_warning, log_info


try:
    with EventProcessor() as event_processor:
    	event_processor.process_corp_generate_creds()
except Exception as e:
    print("Exception", e)
    log_error("generate_creds processing exception: " + str(e))
    raise

