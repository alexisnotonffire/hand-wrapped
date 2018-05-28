from google.cloud import bigquery
from io import BytesIO

class BigQueryLoader:
    """
    Create a BigQuery client that can upload data from a file

    Args:
        location (str): 'US' or 'EU', must match dataset location
        dataset (str): The target dataset
        table (str): The target table
        file (str): String path of the datafile (inc. type)

    """

    def __init__(self, location, dataset, table, file):
        self.client = bigquery.Client()
        self.location = location
        self.dataset = self.client.dataset(dataset)
        self.table = self.dataset.table(table)
        self.file = file
        self.jobConfig = None
        self.job = None

    # TODO: Update to allow different configs
    def configureJob(self):
        jobConfig = bigquery.LoadJobConfig()
        jobConfig.autodetect = True
        jobConfig.schemaUpdateOptions=[
            'ALLOW_FIELD_ADDITION',
            'ALLOW_FIELD_RELAXATION'
        ]
        jobConfig.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        self.jobConfig = jobConfig
        return jobConfig

    def run(self):
        with open(self.file, 'r') as input:
            self.job = self.client.load_table_from_file(
                BytesIO(input.read().encode('utf-8')),
                self.table,
                location=self.location,
                job_config=self.jobConfig
            ).result()
