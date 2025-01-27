<details><summary style="font-size:20px;color:Orange">Lecture-Slides-Screenshots</summary>

![sc0](./screenshots/screenshot.png)
![sc1](./screenshots/screenshot%201.png)
![sc1](./screenshots/screenshot%202.png)
![sc1](./screenshots/screenshot%203.png)
![sc1](./screenshots/screenshot%204.png)
![sc1](./screenshots/screenshot%205.png)
![sc1](./screenshots/screenshot%206.png)
![sc1](./screenshots/screenshot%207.png)
![sc1](./screenshots/screenshot%208.png)
![sc1](./screenshots/screenshot%209.png)
![sc1](./screenshots/screenshot%2010.png)

</details>

-   **Agenda**: Data Lake construction using AWS Glue and Amazon Athena

    -   Data extraction from Amazon RDS databases
    -   Raw data storage in Bronze Area
    -   Data cleansing and augmentation in Silver Area
    -   Creation of curated data sets in Gold Area
    -   Query optimization in Amazon Athena for efficient data retrieval

-   **Part One: Demonstration Overview**

    -   `Cloud Formation folder`: Two cloud formation stacks

        -   `First stack`: creates resources for data lake
            -   AWS glue crawlers
            -   AWS glue connections
            -   AWS glue jobs
            -   AWS glue data catalog
            -   Two Amazon S3 buckets (one for Glue, one for data lake)
        -   `Second stack`: creates three Amazon RDS databases

    -   `Glue script`
        -   14 glue jobs: 7 bronze, 7 silver
    -   `SQL scripts folder`
        -   Amazon Athena commands for part four
        -   Three scripts for database commands (MS SQL, MySQL, Postgres SQL)
        -   Script to create additional sales data (up to 175,000 records)
    -   `README file`: contains all commands for the demonstration

-   **Step One:** Cataloging Data Sources

    -   AWS glue crawlers and connections for three data sources (Postgres, MySQL, SQL Server)
        -   Catalog seven tables in three Amazon RDS databases
            -   `MS SQL database (CRM system)`: tickit database, CRM schema, `users` table
            -   `MySQL database (E-commerce system)`: E comm database, three tables (`date`, `listing`, `sales`)
            -   `Postgres SQL database (Event management system)`: tickit database, EMS schema, three tables (`category`, `venue`, `event`)
        -   Start three crawlers and catalog metadata into AWS glue data catalog

-   **Step Two:** Copying Data to Data Lake

    -   Copy data from three data sources to Amazon S3 (bronze area)
        -   Seven AWS glue jobs extract data from databases to S3 bucket (bronze/raw area)
    -   AWS S3 bucket (open data lakes)
        -   Bronze sub-directory within tickit directory
            -   Seven subdirectories (one per table)
    -   AWS glue data catalog update
        -   14 tables (7 source, 7 bronze)
        -   Metadata includes physical location in S3, schema, etc.

-   **Step Three:** Transforming Data (Bronze to Silver)

    -   Perform ETL/ELT on bronze data
        -   Seven AWS glue jobs (Apache Spark)
            -   Transform raw data to silver/augmented area
            -   Basic transformations (e.g., removing columns, checking for nulls, converting strings to integers)
    -   Amazon S3 bucket update
        -   Silver sub-directory within tickit directory
            -   Seven subdirectories (one per table)
    -   AWS glue data catalog update
        -   21 tables (7 source, 7 bronze, 7 silver)

-   **Step Four**
    -   Option: AWS Glue Jobs
        -   Alternative: Amazon Athena
            -   SQL-based interactive analytics
            -   Uses AWS Glue Data Catalog
            -   Create Table As Select (CTAS) Queries
                -   Creates new tables in Glue Data Catalog
                -   Writes data back to Amazon S3 in gold/curated area

### Amazon Athena Commands

-   **Commands Overview**
    -   Two Create Table As Select (CTAS) Queries for Sales Data
        -   Sales by Category
        -   Sales by Date
    -   Purpose
        -   Data Scientists' Queries: Category-based
            -   Specific categories, groups, names
        -   Data Scientists' Queries: Date-based
            -   Year, month-based queries

### CTAS Statement: Sales by Category

-   **Process**
    -   Define files in S3 data lake
        -   Format: Apache Parquet
        -   Compression: Stampy
    -   External Location: S3 Gold Area
        -   Partition: Category Group, Category Name
    -   Bucketing: Count of One
        -   Single file per bucket
    -   SELECT Statement
        -   Join across silver tables (listings, user, event, date)
        -   SQL functions: concat, rounding, casting
    -   Expected Outcome
        -   Curated data set for category-based queries

### Execution and Result

-   **Execution**
    -   Athena Console
    -   Glue Data Catalog: Data Lake Demo
    -   Paste and run CTAS query
-   **Result**
    -   Completion in 57.9 seconds
    -   12.5 MB of data scanned
-   **S3 Bucket Structure**
    -   Gold Sales by Category
        -   Category Groups: Shows, Concerts
        -   Category Names: Plays, Operas, Musicals (under Shows)
    -   Single file per category name (e.g., 6.3 MB)

### Content Verification

-   **File Contents**
    -   Calendar date, price, quantity, sales, commission, event name, buyer, seller, category
-   **Data Catalog Update**
    -   New partitions: Category Group, Category Name

### CTAS Statement: Sales by Date

-   **Process**
    -   Similar to Sales by Category
    -   Partition: Year, Month
    -   SELECT Statement
        -   Similar joins and SQL functions
-   **Execution and Result**
    -   Completion in 15 seconds
    -   12.5 MB of data scanned
-   **S3 Bucket Structure**
    -   Gold Sales by Date
        -   Year 2020
        -   Months 1-12
    -   Single file per month (e.g., 2.7 MB)

### Content Verification

-   **File Contents**
    -   Similar to Sales by Category
-   **Data Catalog Update**
    -   New partitions: Year, Month

### Medallion Architecture Overview

-   **Bronze Area**
    -   Raw data extracted from databases
-   **Silver Area**
    -   Refined/cleansed data
-   **Gold Area**
    -   Curated data sets
        -   Sales by Category
        -   Sales by Date

### Query Optimization in Amazon Athena

-   **Inefficient Query Example**
    -   `SELECT *` from Gold Sales by Category
    -   Scans 27 MB of data
    -   Completion: 2.5 seconds
-   **Optimized Query Example**
    -   Specify columns: calendar date, sales, commission
    -   Scans 5.39 MB of data
    -   Completion: 1.7 seconds
-   **Partition-Based Query**
    -   `WHERE` clause: Category Group of Shows, Category Name of Operas
    -   Scans 726 KB of data
    -   Completion: Faster and more efficient

### Final Demonstration

-   **Gold Sales by Date Query**
    -   Use partitions: Year 2020, Month 6
    -   Scans 1.09 MB of data
    -   Completion: 1.7 seconds
    -   Comparison without `WHERE` clause
        -   Scans 12 MB of data

### Summary

-   **Process Recap**
    -   Data Lake construction using AWS Glue and Amazon Athena
    -   Data extraction from Amazon RDS databases
    -   Raw data storage in Bronze Area
    -   Data cleansing and augmentation in Silver Area
    -   Creation of curated data sets in Gold Area
    -   Query optimization in Amazon Athena for efficient data retrieval
