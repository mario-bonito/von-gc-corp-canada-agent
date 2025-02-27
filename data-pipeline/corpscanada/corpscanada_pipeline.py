import os
from data_integration.pipelines import Pipeline, Task
from data_integration.ui.cli import run_pipeline
import mara_db.auto_migration
import mara_db.config
import mara_db.dbs
import data_integration
import data_integration.config
from mara_app.monkey_patch import patch
from corpscanada.corpscan_pipelines import corpscanada_root_pipeline
from corpscanada.rocketchat_hooks import log_error, log_warning, log_info


patch(data_integration.config.system_statistics_collection_period)(lambda: 15)

@patch(data_integration.config.root_pipeline)
def root_pipeline():
    return corpscanada_root_pipeline()

mara_host = os.environ.get('MARA_DB_HOST', 'corpscanadadb')
mara_database = os.environ.get('MARA_DB_DATABASE', 'mara_db')
mara_port = os.environ.get('MARA_DB_PORT', '5432')
mara_user = os.environ.get('MARA_DB_USER', 'mara_db')
mara_password = os.environ.get('MARA_DB_PASSWORD')

try:
    log_info("Starting corpscanada_event_processor ...")
    mara_db.config.databases \
        = lambda: {'mara': mara_db.dbs.PostgreSQLDB(user=mara_user, password=mara_password, host=mara_host, database=mara_database, port=mara_port)}

    (child_pipeline, success) = data_integration.pipelines.find_node(['corpscanada_event_processor'])
    if success:
        run_pipeline(child_pipeline)
        log_info("Ran corpscanada_event_processor - complete.")
    else:
        print("Pipeline not found")
        log_error("Pipeline not found for:" + "corpscanada_event_processor")
except Exception as e:
    print("Exception", e)
    log_error("corpscanada_event_processor processing exception: " + str(e))
    raise
