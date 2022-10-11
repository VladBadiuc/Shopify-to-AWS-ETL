# Shopify-to-AWS-ETL
Alternative way to store data from Shopify into an AWS S3 bucket using and Change Data Capture ETL pipeline

0. Motivation and basic explanation of usage

1. Extract data from Shopify

2. AWS RDS to temporary S3 via DMS

3. AWS Glue invokation via Lambda

4. Glue Script explanation and final load



***********************************************************************************************************************************************************

0. Motivation and basic explanation of usage

I wanted to find an alternative way to store the data of my Shopify customers and orders so I decided to use my knowledge of ETL pipelines for this project. I consider Change Data Capture (CDC) to be the best structure for this functionality because I want to store the data itself and all the changes.

I opened a blank Shopify store to avoid leaking any sensitive data. The API and MySQL access keys have been deleted and need to be set at credentials.py


The main data I want to store is customer and orders data, so I create random customers from my Shopify platform, I move that data to my Python script running on an EC2 instance. This .py script is going to extract the customer data via API calls, transform it into tables and push into a RDS MySQL database.
When I have the fresh info appended in MySQL I need to push it into a temporary S3 bucket, for this I need to use Data Migration Service (AWS DMS).
A lambda function will be triggered everytime a new object is created in this temporary bucket. This lambda will pass parameters to a GLUE script.
This final script is for transforming the data into a standardized format and finally updating the .csv in the final bucket.

Simplified schema:
Shopify --(API)--> Python Script(EC2) --> RDS(MySQL) --(DMS)--> temp S3 --(lambda)--> Glue --(create or append)--> final S3

***********************************************************************************************************************************************************


1. Extract data from Shopify

The first step in any data pipeline is extraction of data. This process will be accomplish with the API calls from the official Shopify API. It is needed to own a store and have the administrator keys, also it's needed to give permissions to the data we want to manage.

For the connection to the AWS RDS MySQL database an auxiliary class is implementedin MySQL_class.py, with the help of the library pymysql.
Two main methods can be used from this class, execute() for running SQL queries and fetch() which will return objects.

The file AWS_RDS_MySQL.py is supposed to be run on a EC2 instance, the script will make an API call every minute to check for updates on the data, in case there is any change it will format the updates and query them into MySQL (RDS).
It is not needed to reserve a huge EC2 instance, the smallest one is more than enough for this task and for cost efficieny.

For the visualization of proper loading into MySQL I used the MySQL Workbench to check if everything works as it should.

***********************************************************************************************************************************************************


2. AWS RDS to temporary S3 via DMS

In this second step we need to migrate the data into a temporary S3 bucket. Everytime MySQL database is updated a new csv file will be created in the temporary bucket. For this step it is needed to use AWS DMS:

-First we need to create two endpoints. The source endpoint from MySQL (we need to check the RDS box for an easier configuration), and the target endpoint which is going to be the temporary S3 bucket.

-A replication instance with the minimal 'Instance class', dms.t2.small is enough.

-A migration task of type 'Migrate data and replicate ongoing changes'.

***********************************************************************************************************************************************************


3. AWS Glue invokation via Lambda

At this point every new query in MySQL should produce a new .csv file in the temporary S3 bucket. This event has to trigger a lambda function.
It is essential to set the lambda trigger as the temporary S3 bucket. Not necessary to set the target.

The mission of this lambda function is to get the bucketName and the fileName and pass them as --parameters to the Glue Job. The library boto3 will be needed. It will help us create a client('glue') and glue.start_job_run().
















