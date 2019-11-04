#!/usr/bin/python

import psycopg2
import datetime
import json
from corpscanada.config import config
from corpscanada.eventprocessor import EventProcessor
from corpscanada.eventprocessor import corp_credential, corp_schema, corp_version
from corpscanada.eventprocessor import addr_credential, addr_schema, addr_version
from corpscanada.eventprocessor import dba_credential, dba_schema, dba_version
from corpscanada.corporationscanada import system_type, MIN_START_DATE


with EventProcessor() as event_processor:
    # insert last event
    event_processor.insert_last_event(system_type, 0, MIN_START_DATE)

    print("Seeded initial event processor data")

