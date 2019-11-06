from data_integration.pipelines import Pipeline, Task
from data_integration.commands.python import ExecutePython

def corpscanada_root_pipeline():
    import corpscanada

    parent_pipeline = Pipeline(
        id = 'holder_for_pipeline_versions',
        description = 'Holder for the different versions of the Corporations Canada pipeline.')

    parent_pipeline.add(corpscanada_pipeline())
    parent_pipeline.add(corpscanada_pipeline_status())

    init_pipeline = Pipeline(
        id = 'initialization_and_load_tasks',
        description = 'One-time initialization and data load tasks')

    init_pipeline.add(db_init_pipeline())
    init_pipeline.add(corpscanada_pipeline_initial_load())
    init_pipeline.add(corpscanada_pipeline_post_credentials())

    parent_pipeline.add(init_pipeline)

    test_pipeline = Pipeline(
        id = 'test_and_demo_tasks',
        description = 'Holder for test and demo tasks.')

    test_pipeline.add(corpscanada_init_test_data())
    test_pipeline.add(corpscanada_test_corps())
    test_pipeline.add(corpscanada_pipeline_single_thread())
    test_pipeline.add(corpscanada_pipeline_jsonbender())

    parent_pipeline.add(test_pipeline)

    return parent_pipeline

def corpscanada_pipeline():
    import corpscanada

    pipeline1 = Pipeline(
        id='corpscanada_event_processor',
        description='A pipeline that processes BC Registries events and generates credentials.')

    sub_pipeline1_2 = Pipeline(id='load_and_process_corpscanada_data', description='Load BC Reg data and generate credentials')
    sub_pipeline1_2.add(Task(id='register_un_processed_events', description='Register un-processed events',
                          commands=[ExecutePython('./corpscanada/find-unprocessed-events.py')]))
    sub_pipeline1_2.add(Task(id='load_corpscanada_data', description='Load BC Registries data',
                          commands=[ExecutePython('./corpscanada/process-corps-generate-creds.py')]), ['register_un_processed_events'])
    sub_pipeline1_2.add(Task(id='create_corpscanada_credentials', description='Create credentials',
                          commands=[ExecutePython('./corpscanada/generate-creds.py')]), ['load_corpscanada_data'])
    pipeline1.add(sub_pipeline1_2)

    sub_pipeline1_3 = Pipeline(id='submit_corpscanada_credentials', description='Submit BC Reg credentials to P-X')
    sub_pipeline1_3.add(Task(id='submit_credentials', description='Submit credentials',
                          commands=[ExecutePython('./corpscanada/submit-creds.py')]))
    pipeline1.add(sub_pipeline1_3, ['load_and_process_corpscanada_data'])

    sub_pipeline1_4 = Pipeline(id='populate_evp_audit_table', description='Populate Event Processor Audit Table')
    sub_pipeline1_4.add(Task(id='populate_audit_table', description='Populate Audit Table',
                          commands=[ExecutePython('./corpscanada/populate_audit_table.py')]))
    pipeline1.add(sub_pipeline1_4, ['submit_corpscanada_credentials'])

    return pipeline1

def corpscanada_pipeline_single_thread():
    import corpscanada

    pipeline1 = Pipeline(
        id='corpscanada_event_processor_single_thread',
        description='A pipeline that processes BC Registries events and generates credentials.')

    sub_pipeline1_2 = Pipeline(id='load_and_process_corpscanada_data_single_thread', description='Load BC Reg data and generate credentials')
    sub_pipeline1_2.add(Task(id='register_un_processed_events_single_thread', description='Register un-processed events',
                          commands=[ExecutePython('./corpscanada/find-unprocessed-events.py')]))
    sub_pipeline1_2.add(Task(id='load_corpscanada_data_single_thread', description='Load BC Registries data',
                          commands=[ExecutePython('./corpscanada/register_un_processed_events')]), ['register_un_processed_events_single_thread'])
    pipeline1.add(sub_pipeline1_2)

    sub_pipeline1_3 = Pipeline(id='submit_corpscanada_credentials_single_thread', description='Submit BC Reg credentials to P-X')
    sub_pipeline1_3.add(Task(id='submit_credentials_single_thread', description='Submit credentials',
                          commands=[ExecutePython('./corpscanada/submit-creds-single-thread.py')]))
    pipeline1.add(sub_pipeline1_3, ['load_and_process_corpscanada_data_single_thread'])

    return pipeline1

def corpscanada_pipeline_initial_load():
    import corpscanada

    pipeline1 = Pipeline(
        id='corpscanada_corp_loader',
        description='A pipeline that does the initial data load and credentials for all corporations.')

    sub_pipeline1_2 = Pipeline(id='load_and_process_corpscanada_corps', description='Load Active BC Reg corps and generate credentials')
    sub_pipeline1_2.add(Task(id='register_un_processed_corps', description='Register un-processed active corps',
                          commands=[ExecutePython('./corpscanada/find-unprocessed-corps_actve.py')]))
    sub_pipeline1_2.add(Task(id='load_corpscanada_data_a', description='Load BC Registries data',
                          commands=[ExecutePython('./corpscanada/process-corps-generate-creds.py')]), ['register_un_processed_corps'])
    pipeline1.add(sub_pipeline1_2)

    return pipeline1

def corpscanada_pipeline_post_credentials():
    import corpscanada

    pipeline1 = Pipeline(
        id='corpscanada_credential_poster',
        description='A pipeline that posts generated credentials to TOB.')

    sub_pipeline1_3 = Pipeline(id='submit_corpscanada_credentials_a', description='Submit BC Reg credentials to P-X')
    sub_pipeline1_3.add(Task(id='submit_credentials_a', description='Submit credentials',
                          commands=[ExecutePython('./corpscanada/submit-creds.py')]))
    pipeline1.add(sub_pipeline1_3)

    sub_pipeline1_4 = Pipeline(id='populate_evp_audit_table_a', description='Populate Event Processor Audit Table')
    sub_pipeline1_4.add(Task(id='populate_audit_table_a', description='Populate Audit Table',
                          commands=[ExecutePython('./corpscanada/populate_audit_table.py')]))
    pipeline1.add(sub_pipeline1_4, ['submit_corpscanada_credentials_a'])

    return pipeline1

def corpscanada_pipeline_status():
    import corpscanada

    pipeline = Pipeline(
        id='corpscanada_pipeline_status',
        description='Display overall event processing status.')

    pipeline.add(Task(id='display_pipeline_status', description='Display status of the overall pipeline processing status',
                        commands=[ExecutePython('./corpscanada/display_pipeline_status.py')]))
    # remove these from the pipeline due to issues connecting to DB's on openshift
    #pipeline.add(Task(id='display_pipeline_stats', description='Display stats of each stage in the pipeline processing',
    #                    commands=[ExecutePython('./corpscanada/display_processed_corps_counts.py')]))
    pipeline.add(Task(id='display_event_processor_stats', description='Display stats of each event processor stage',
                        commands=[ExecutePython('./corpscanada/display_event_processor_counts.py')]))

    return pipeline

def db_init_pipeline():
    import corpscanada

    pipeline = Pipeline(
      id = 'corpscanada_db_init',
      description = 'Initialize BC Registries Event Processor database')

    pipeline.add(Task(id='create_tables', description='Create event processing tables',
                        commands=[ExecutePython('./corpscanada/create.py')]))
    pipeline.add(Task(id='initialize_tables', description='Insert configuration data',
                        commands=[ExecutePython('./corpscanada/insert.py')]), ['create_tables'])

    return pipeline

def corpscanada_init_test_data():
    import corpscanada

    pipeline = Pipeline(
        id='corpscanada_test_data',
        description='A pipeline that initializes event processor database for testing.')

    pipeline.add(Task(id='register_test_corps', description='Insert some test data for processing',
                        commands=[ExecutePython('./corpscanada/insert-test.py')]))

    return pipeline

def corpscanada_test_corps():
    import corpscanada

    pipeline = Pipeline(
        id='corpscanada_test_corps',
        description='A pipeline that queues up a small set of test corporations.')

    pipeline.add(Task(id='register_test_corps', description='Register some test corps for processing',
                        commands=[ExecutePython('./corpscanada/find-test-corps.py')]))

    return pipeline

def corpscanada_pipeline_jsonbender():
    import corpscanada

    pipeline2 = Pipeline(
        id='corpscanada_event_processor_json_transform_demo',
        description='A demo pipeline that processes events and generates credentials using JSONBender.')

    sub_pipeline2_2 = Pipeline(id='load_and_process_corpscanada_data', description='Load Corporations Canada data and generate credentials')
    sub_pipeline2_2.add(Task(id='register_un_processed_events', description='Register un-processed events',
                          commands=[ExecutePython('./corpscanada/find-unprocessed-events.py')]))
    sub_pipeline2_2.add(Task(id='load_corpscanada_data', description='Load Corporations Canada data',
                          commands=[ExecutePython('./corpscanada/process-corps.py')]), ['register_un_processed_events'])
    sub_pipeline2_2.add(Task(id='create_credentials_jsonbender', description='Create credentials using JSONBender transform',
                          commands=[ExecutePython('./corpscanada/generate-creds-bender.py')]), ['load_corpscanada_data'])
    pipeline2.add(sub_pipeline2_2)

    sub_pipeline2_3 = Pipeline(id='submit_corpscanada_credentials', description='Submit Corporations Canada credentials to P-X')
    sub_pipeline2_3.add(Task(id='submit_credentials', description='Submit credentials',
                          commands=[ExecutePython('./corpscanada/submit-creds.py')]))
    pipeline2.add(sub_pipeline2_3, ['load_and_process_corpscanada_data'])

    return pipeline2

