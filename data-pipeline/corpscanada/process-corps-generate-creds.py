#!/usr/bin/python
import psycopg2
import datetime
import json
import decimal
import os
from corpscanada.config import config
from corpscanada.eventprocessor import EventProcessor, CORP_TYPES_IN_SCOPE
from corpscanada.rocketchat_hooks import log_error, log_warning, log_info


try:
    with EventProcessor() as event_processor:
        # check for a (comma-delimited) list of corp types to process
        corp_types = os.environ.get('CORP_TYPES_SCOPE', '')

        if not corp_types or 0 == len(corp_types):
            event_processor.process_corp_event_queue_and_generate_creds(True)
        else:
            corp_types = corp_types.split(",")
            corp_types_scope = {}
            for corp_type in corp_types:
                if corp_type in CORP_TYPES_IN_SCOPE:
                    corp_types_scope[corp_type] = CORP_TYPES_IN_SCOPE[corp_type]
            event_processor.process_corp_event_queue_and_generate_creds(True, corp_types=corp_types_scope)
except Exception as e:
    print("Exception", e)
    log_error("process_corps_generate_creds processing exception: " + str(e))
    raise


