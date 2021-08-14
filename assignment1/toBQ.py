from google.cloud import bigquery, storage

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "assignment1.output_geomap"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("id", "STRING"),
        bigquery.SchemaField("file_name", "STRING"),
        bigquery.SchemaField("file_index", "INTEGER"),
        bigquery.SchemaField("img_type", "STRING"),
        bigquery.SchemaField("time_utc", "TIMESTAMP"),
        bigquery.SchemaField("minute_offsets", "STRING"),
        bigquery.SchemaField("episode_id", "FLOAT"),
        bigquery.SchemaField("event_id", "FLOAT"),
        bigquery.SchemaField("event_type", "STRING"),
        # bigquery.SchemaField("llcrnrlat", "FLOAT"),
        # bigquery.SchemaField("llcrnrlon", "FLOAT"),
        # bigquery.SchemaField("urcrnrlat", "FLOAT"),
        # bigquery.SchemaField("urcrnrlon", "FLOAT"),
        bigquery.SchemaField("proj", "STRING"),
        bigquery.SchemaField("size_x", "INTEGER"),
        bigquery.SchemaField("size_y", "INTEGER"),
        bigquery.SchemaField("height_m", "FLOAT"),
        bigquery.SchemaField("width_m", "FLOAT"),
        bigquery.SchemaField("data_min", "FLOAT"),
        bigquery.SchemaField("data_max", "FLOAT"),
        bigquery.SchemaField("pct_missing", "FLOAT"),
        bigquery.SchemaField("STATE", "STRING"),
        bigquery.SchemaField("STATE_FIPS", "FLOAT"),
        bigquery.SchemaField("CZ_TYPE", "STRING"),
        bigquery.SchemaField("CZ_FIPS", "FLOAT"),
        bigquery.SchemaField("CZ_NAME", "STRING"),
        bigquery.SchemaField("WFO", "STRING"),
        bigquery.SchemaField("CZ_TIMEZONE", "STRING"),
        bigquery.SchemaField("INJURIES_DIRECT", "FLOAT"),
        bigquery.SchemaField("INJURIES_INDIRECT", "FLOAT"),
        bigquery.SchemaField("DEATHS_DIRECT", "FLOAT"),
        bigquery.SchemaField("DEATHS_INDIRECT", "FLOAT"),
        bigquery.SchemaField("DAMAGE_PROPERTY", "STRING"),
        bigquery.SchemaField("DAMAGE_CROPS", "STRING"),
        bigquery.SchemaField("SOURCE", "STRING"),
        bigquery.SchemaField("MAGNITUDE", "FLOAT"),
        bigquery.SchemaField("MAGNITUDE_TYPE", "STRING"),
        bigquery.SchemaField("FLOOD_CAUSE", "STRING"),
        bigquery.SchemaField("CATEGORY", "FLOAT"),
        bigquery.SchemaField("TOR_F_SCALE", "STRING"),
        bigquery.SchemaField("TOR_LENGTH", "FLOAT"),
        bigquery.SchemaField("TOR_WIDTH", "FLOAT"),
        bigquery.SchemaField("TOR_OTHER_WFO", "STRING"),
        bigquery.SchemaField("TOR_OTHER_CZ_STATE", "STRING"),
        bigquery.SchemaField("TOR_OTHER_CZ_FIPS", "FLOAT"),
        bigquery.SchemaField("TOR_OTHER_CZ_NAME", "STRING"),
        bigquery.SchemaField("BEGIN_RANGE", "FLOAT"),
        bigquery.SchemaField("BEGIN_AZIMUTH", "STRING"),
        bigquery.SchemaField("BEGIN_LOCATION", "STRING"),
        bigquery.SchemaField("END_RANGE", "FLOAT"),
        bigquery.SchemaField("END_AZIMUTH", "STRING"),
        bigquery.SchemaField("END_LOCATION", "STRING"),
        # bigquery.SchemaField("BEGIN_LAT", "FLOAT"),
        # bigquery.SchemaField("BEGIN_LON", "FLOAT"),
        # bigquery.SchemaField("END_LAT", "FLOAT"),
        # bigquery.SchemaField("END_LON", "FLOAT"),
        bigquery.SchemaField("EPISODE_NARRATIVE", "STRING"),
        bigquery.SchemaField("EVENT_NARRATIVE", "STRING"),
        bigquery.SchemaField("llcrnr", "STRING"),
        bigquery.SchemaField("urcrnr", "STRING"),
        bigquery.SchemaField("BEGIN_loc", "STRING"),
        bigquery.SchemaField("END_loc", "STRING")
    ],
    # write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    # skip_leading_rows=1,
    # The source format defaults to CSV, so the line below is optional.
    source_format=bigquery.SourceFormat.CSV,
    field_delimiter="^"
)

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "assignment1-data"
    res = []
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        # print(blob.name)
        if blob.name.startswith("afterPipeline") and blob.name.endswith(".csv"):
            res.append('gs://assignment1-data/' + blob.name)
    
    return res

uri = list_blobs("assignment1-data")

for i in uri:
    load_job = client.load_table_from_uri(
        i, table_id, 
        job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
print("Loaded {} rows.".format(destination_table.num_rows))