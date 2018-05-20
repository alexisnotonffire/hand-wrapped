from google.cloud import bigquery

class BigQueryLoader:
    """
    Create a BigQuery client that can upload data from a file

    Args:
        location (str): 'US' or 'EU', must match dataset location
        dataset (str): The target dataset
        table (str): The target table
        file (str): String path of the datafile (inc. type)

    """

    def __init__(location, dataset, table, file):
        self.location = location
        self.dataset = dataset
        self.table = table
        self.file = file
        self.jobConfig = None
        self.job = None

    # TODO: Update to allow different configs
    def configureJob():
        jobConfig = bigquery.LoadJobConfig()
        jobConfig.autodetect = True
        jobConfig.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        self.jobConfig = jobConfig

    def run(location, dataset, table, file):
        self.job = client.load_table_from_file(
            file,
            table,
            location=location,
            job_config=jobConfig
        )
