# Assignment1 Report
### Overview
In this Project, I became more adept at using [Apache.beam](https://beam.apache.org/) and [Google Cloud Platform](https://console.cloud.google.com/). I combined satellite data and storm data via Python scripts and pipeline. 

It was a big challenge. Because I think parameter passing in [Apache.beam](https://beam.apache.org/) pipeline is a little strange. For example, I use `"Data Combine" >> beam.FlatMap(combine, beam.pvalue.AsDict(stormEvents))` to combine the files. I defined `combine` function as below: 
``` python
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
```

I don’t know how `beam.FlatMap` works to pass two parameters to `combine` function. 

However, actually, [Apache.beam](https://beam.apache.org/) pipeline is a great tool for big data analytics. Because combine with the Dataflow in [Google Cloud Platform](https://console.cloud.google.com/), I can see the job graph clearly. And compared to processing data by Python script, the command of [Apache.beam](https://beam.apache.org/) pipeline is more concise and easier to understand.

The [Google Cloud Platform](https://console.cloud.google.com/) is also a useful tool to analyze big data. In this assignment, the first problem I encountered was the data size was extremely large. The data took up too much local space. Moving these data to cloud is a good choice. After getting familiar with the Platform, I think, it is very easy to manage my workflow in the Platform. I can upload all data to the Cloud Storage Buckets. I can edit my codes in Cloud shell Editor. I can run my codes in Cloud shell Terminal and put the output data into the Cloud Storage Buckets. And the visualization is also attractive. Like I said, I can see the [Dataflow graph](https://console.cloud.google.com/dataflow/jobs/us-central1/2021-07-09_21_02_22-8307640423329231949?pageState=(%22dfTime%22:(%22s%22:%222021-07-10T04:02:23.005Z%22,%22e%22:%222021-07-10T04:08:44.034Z%22))&project=hardy-portal-318606) in the Platform. After loading my output data into BigQuery, I can see my data in the Platform directly. By means of [Google Data Studio](https://datastudio.google.com/), BigQuery Data can also be visualized. And in [Google Data Studio](https://datastudio.google.com/), I can do some simple things with the data, such as filter, sort and transferring data format. It is helpful for feature engineering before build machine learning models if needed. 
- - -
### Combine Method
In this assignment, I combined satellite data and storm data by following steps.
- I used the storm data named ***StormEvents_details-ftp_v1.0_d2018_c20210604.csv.gz*** to create a dictionary. The keys are <kbd>EVENT_ID</kbd> column in the storm data at first. But the <kbd>EVENT_ID</kbd> are float format, so I add a **"S"** before <kbd>EVENT_ID</kbd> as the key. And about the value of dictionary, I used columns apart from <kbd>EVENT_ID</kbd> and other columns which duplicate with the satellite data. 
- I loaded the satellite data called ***CATALOG.csv*** into pipeline. I had deleted some invalid data in ***CATALOG.csv*** before I loaded it. For example, each event in ***CATALOG.csv*** should have five <kbd>img_type</kbd> s, so I removed the data whose number of <kbd>img_type</kbd> is less than five. 
- After that, I combined satellite data and storm data together via [Apache.beam](https://beam.apache.org/) command `"Data Combine" >> beam.FlatMap(combine, beam.pvalue.AsDict(stormEvents))`.
- - -
### Challenges
There are many challenges working with this architecture. 
- Firstly, as I mentioned above, the parameter passing in [Apache.beam](https://beam.apache.org/) pipeline is a little strange to me. 
- Secondly, when I encountered some trouble about [Apache.beam](https://beam.apache.org/) and [Google Cloud Platform](https://console.cloud.google.com/), I could find limited resources in stackoverflow, compare to some Python troubles. So I had to read the official documents of [Apache.beam](https://beam.apache.org/) and [Google Cloud Platform](https://console.cloud.google.com/) carefully, sometimes even source codes of some commands. It was a boring process, but efficient. It made me get a higher-level understanding of these tools. When I was reading the documents and source codes, I was not just focus on how to solve the troubles, but much deeper. It made me know more about inside commands and tools about how it works.
- - -
### Benefit and Cost
Except for the benefit what I mentioned above, the other benefit of this architecture is that it doesn’t occupy any local storage space or CPU. It is very important to deal with Big Data for individual and some companies. Because Big Data always means hundreds of GBs or TBs, even PBs. It is impossible for us, most individuals and companies, to buy a professional server for data processing. Then [Google Cloud Platform](https://console.cloud.google.com/) is a great choice. And the Platform can be combined well with [Apache.beam](https://beam.apache.org/) pipeline. The job Dataflow can be displayed by these tools. 

I also found this architecture in [Google Cloud Platform](https://console.cloud.google.com/) is much slower than run same codes locally. But this issue may be caused by that I only used the default compute engine. There are also many high-performance machines, but much more expensive. I am in a free trial. And I think the performance of default compute engine is acceptable. So I didn’t buy another machine.
- - -
To sum up, I think this architecture via [Apache.beam](https://beam.apache.org/) pipeline and [Google Cloud Platform](https://console.cloud.google.com/) is appropriate for this project. You can see my [Dataflow](https://console.cloud.google.com/dataflow/jobs/us-central1/2021-07-09_21_02_22-8307640423329231949?pageState=(%22dfTime%22:(%22s%22:%222021-07-10T04:02:23.005Z%22,%22e%22:%222021-07-10T04:08:44.034Z%22))&project=hardy-portal-318606) and [brief report](https://datastudio.google.com/s/hjq0Q7qP-Lk) of this project in [Google Data Studio](https://datastudio.google.com/).