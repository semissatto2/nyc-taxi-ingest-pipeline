## Question 1. Understanding docker first run
```bash
docker run -it --entrypoint bash python:3.12.8
```

```bash
pip list
```

Answer: <mark>24.3.1</mark>

### Question 2. Understanding Docker networking and docker-compose

Answer: <mark> db:5432 </mark>

## Question 3. Trip Segmentation Count

Answer: <mark>104,793; 198,924; 109,603; 27,678; 35,189</mark> 
```sql
    SELECT 
    SUM(CASE WHEN trip_distance <= 1 THEN 1 ELSE 0 END) AS TOTAL_TRIPS_UP_TO_1_MILE,
    SUM(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 ELSE 0 END) AS TOTAL_TRIPS_BETWEEN_1_AND_3_MILES,
    SUM(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 ELSE 0 END) AS TOTAL_TRIPS_BETWEEN_3_AND_7_MILES,
    SUM(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 ELSE 0 END) AS TOTAL_TRIPS_BETWEEN_7_AND_10_MILES,
    SUM(CASE WHEN trip_distance > 10 THEN 1 ELSE 0 END) AS TOTAL_TRIPS_OVER_10_MILES
    FROM ny_taxi_trips
    WHERE lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01'
```
## Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Answer: <mark>2019-10-31</mark>
```sql
    SELECT
    SUBSTR(lpep_pickup_datetime, 1, 10) AS date,
    trip_distance
    FROM ny_taxi_trips
    ORDER BY trip_distance DESC
    LIMIT 3
```
## Question 5. Three biggest pickup zones
Which where the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?

Consider only lpep_pickup_datetime when filtering by date.

Answer: <mark>East Harlem North, East Harlem South, Morningside Heights</mark>
```sql
    SELECT
    t1."PULocationID",
    t2."Zone",
    SUM(total_amount) AS total_amount
    FROM ny_taxi_trips t1
    LEFT JOIN ny_taxi_zones t2
    ON t1."PULocationID" = t2."LocationID"
    WHERE SUBSTR(lpep_pickup_datetime, 1, 10) = '2019-10-18'
    GROUP BY 1, 2
    HAVING SUM(total_amount) > 13000
    ORDER BY total_amount DESC
```
## Question 6. Largest tip
For the passengers picked up in Ocrober 2019 in the zone name "East Harlem North" which was the drop off zone that had the largest tip?

Answer: <mark>JFK Airport</mark>

```sql
    SELECT
    lpep_pickup_datetime,
    t1."PULocationID",
    t1."DOLocationID",
    t2."Zone",
    tip_amount
    FROM ny_taxi_trips t1
    LEFT JOIN ny_taxi_zones t2
    ON t1."DOLocationID" = t2."LocationID"
    WHERE SUBSTR(lpep_pickup_datetime, 1, 7) = '2019-10'
    AND t1."PULocationID" =  74
    ORDER BY tip_amount DESC
```
## Question 7. Terraform Workflow
Which of the following sequences, respectively, describes the workflow for:

1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform

Answer: <mark> terraform init, terraform apply -auto-approve, terraform destroy </mark>
