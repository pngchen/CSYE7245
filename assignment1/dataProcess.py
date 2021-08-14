import apache_beam as beam
import csv

def stormDict(fields):
    delIndex = [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 17, 19, 50]
    return [fields[i] for i in range(len(fields)) if i not in delIndex]

def combine(fields, stormEvent):
    if fields[0] != 'id' and len(fields) == 21:
        if fields[0].startswith("S"):
            eventId = fields[0]
            fields.extend(stormEvent[eventId])
            yield fields
        else:
            fields.extend([""] * 37)
            yield fields
    elif fields[0] == 'id':
        fields.extend(stormEvent["SEVENT_ID"])
        yield fields

def float2geo(fields):
    delIndex = [9, 10, 11, 12, 52, 53, 54, 55]
    if fields[0] != 'id' and len(fields) == 58:
        for i in [9, 11, 52, 54]:
            p = str('Point(' + fields[i + 1] + ' ' + fields[i] + ')')
            # p = str(fields[i + 1] + ',' + fields[i])
            if len(p) > 16:
            # if len(p) > 3:
                fields.append(p)
            else:
                fields.append('')
    elif fields[0] == 'id':
        fields.append('llcrnr')
        fields.append('urcrnr')
        fields.append('BEGIN_loc')
        fields.append('END_loc')

    fields = [fields[i] for i in range(len(fields)) if i not in delIndex]
    return fields

def run(project, bucket, dataset, region):
    argv = [
      '--project={0}'.format(project),
      '--job_name=assignment1',
      '--save_main_session',
      '--staging_location=gs://{0}/staging/'.format(bucket),
      '--temp_location=gs://{0}/temp/'.format(bucket),
    #   '--setup_file=./setup.py',
      '--max_num_workers=8',
      '--region={}'.format(region),
      '--autoscaling_algorithm=THROUGHPUT_BASED',
      '--runner=DataflowRunner'
    ]

    # events_output = '{}:{}.simevents'.format(project, dataset)

    # schema="id:STRING,file_name:STRING,file_index:INTEGER,img_type:STRING,time_utc:TIMESTAMP,minute_offsets:STRING,episode_id:FLOAT,event_id:FLOAT,event_type:STRING,llcrnrlat:FLOAT,llcrnrlon:FLOAT,urcrnrlat:FLOAT,urcrnrlon:FLOAT,proj:STRING,size_x:INTEGER,size_y:INTEGER,height_m:FLOAT,width_m:FLOAT,data_min:FLOAT,data_max:FLOAT,pct_missing:FLOAT,LOCATION_INDEX:STRING,RANGE:STRING,AZIMUTH:STRING,LOCATION:STRING,LATITUDE:STRING,LONGITUDE:STRING,LAT2:STRING,LON2:STRING"

    pipeline = beam.Pipeline(argv=argv)
    stormEvents = (pipeline
                   | 'StormEvents Read' >> beam.io.ReadFromText('gs://assignment1-data/StormEvents_details-ftp_v1.0_d2018_c20210604.csv.gz')
                   | 'StormEvents Fields' >> beam.Map(lambda line: next(csv.reader([line])))
                   | 'StormEvents Dictionary' >> beam.Map(lambda fields: ("S" + fields[7], stormDict(fields)))
                   )

    catalog = (pipeline
                | 'Catalog Read' >> beam.io.ReadFromText('gs://assignment1-data/CATALOG_cleaned.csv')
                | 'Catalog Fields' >> beam.Map(lambda line: next(csv.reader([line])))
                | 'Data Combine' >> beam.FlatMap(combine, beam.pvalue.AsDict(stormEvents))
                | 'Data ToGeography' >> beam.Map(lambda fields: float2geo(fields))
                | 'Data Tostring' >> beam.Map(lambda fields: "^".join(fields))
                | 'Data WriteToCSV' >> beam.io.WriteToText('gs://assignment1-data/afterPipeline', file_name_suffix='.csv') 
                # | 'Data WriteToBigQuery' >> beam.io.WriteToBigQuery(
                #     events_output, schema=schema,
                #     write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                #     create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
        )

    pipeline.run()

if __name__ == '__main__':
   import argparse
   parser = argparse.ArgumentParser(description='Run pipeline on the cloud')
   parser.add_argument('-p','--project', help='Unique project ID', default='hardy-portal-318606')
   parser.add_argument('-b','--bucket', help='Bucket where your data', default='assignment1-data')
   parser.add_argument('-r','--region', help='Region in which to run the Dataflow job. Choose the same region as your bucket.', default='us-central1')
   parser.add_argument('-d','--dataset', help='BigQuery dataset', default='assignment1')
   args = vars(parser.parse_args())

   print ("Correcting timestamps and writing to BigQuery dataset {}".format(args['dataset']))
  
   run(project=args['project'], bucket=args['bucket'], dataset=args['dataset'], region=args['region'])