#!/usr/bin/python
import psycopg2
import datetime
from corpscanada.config import config
from corpscanada.eventprocessor import EventProcessor
from corpscanada.corporationscanada import CorporationsCanada, system_type


with EventProcessor() as event_processor:
    print("Get last processed event")
    prev_event_date = event_processor.get_last_processed_event_date(system_type)
    if prev_event_date is not None:
        prev_event_id = event_processor.get_last_processed_event(prev_event_date, system_type)
    else:
        prev_event_id = 0

    # if the last event is non-zero then we already ran the initial company load
    if 0 < prev_event_id:
        print("Prev event = " + str(prev_event_id) + ", " + str(prev_event_date) + ", skipping initial corps_data_load ...")
    else:
        with BCRegistries() as corporationscanada:
            print("Get last max event")
            max_event_date = corporationscanada.get_max_event_date()
            max_event_id = corporationscanada.get_max_event(max_event_date)

            # get unprocessed corps (there are about 2700)
            print("Get unprocessed corps")
            last_event_dt = corporationscanada.get_event_effective_date(prev_event_id)
            max_event_dt = corporationscanada.get_event_effective_date(max_event_id)
            corps = corporationscanada.get_unprocessed_corps_data_load(prev_event_id, last_event_dt, max_event_id, max_event_dt)

            print("Update our queue")
            event_processor.update_corp_event_queue(system_type, corps, max_event_id, max_event_date)
