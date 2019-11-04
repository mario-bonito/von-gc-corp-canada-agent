#!/usr/bin/python

import psycopg2
from corpscanada.config import config
from corpscanada.eventprocessor import EventProcessor


with EventProcessor() as event_processor:
    event_processor.create_tables()
    print("Created event processor tables")
