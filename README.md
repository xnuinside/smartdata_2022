# smartdata_2022

In this talk I explain why it is totally wrong to compare Prefect vs Apache Airflow & why no sense to try do same pipelines as on Apache Airflow in Prefect. 

So main_flow.py is a bad example by idea. Code is correct & it is working, but it is a bad example of Prefect Usage.


### Up & Run prefect cluster

Already with Agent & DB.

```bash

    docker-compose -f docker-compose-prefect.yml up --build

```


### Login into Prefect UI

go to http://localhost:4200

### Deploy flow 

Create deployment build

```console

    prefect deployment build prefect_flows/main_flow_empty.py:db_data_process_flow --name first

```


Apply build

```console

   prefect deployment apply db_data_process_flow-deployment.yaml

```
