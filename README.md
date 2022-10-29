# smartdata_2022


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


### Up & Run Apache Airflow sample
If you want to up & run Apache Airflow cluster to test airflow dag - use docker-compose from this repo: 





