# EnergyMarketData
# ⚡ EnergyMarketData ETL Pipeline

### Overview
The **EnergyMarketData** project automates the extraction, transformation, and loading (ETL) of electricity market data from AWS S3 into a relational database using **Apache Airflow**.  
The workflow is designed to streamline the data ingestion process and enable **clean, structured, and ready-to-analyze datasets** for downstream analytics and visualization in **Tableau**.

---

## 🧩 Project Architecture

**Tools & Technologies Used**
- **Python** — ETL scripting and data transformation  
- **Apache Airflow** — Workflow orchestration and scheduling  
- **AWS S3** — Raw data storage (CSV files)  
- **PostgreSQL / RDS** — Target database for processed data  
- **SQLAlchemy** — ORM for object–relational mapping  
- **Tableau** — Data visualization and dashboarding  

---

## ⚙️ ETL Workflow Design

The Airflow DAG (`energy_worflow`) runs daily and performs the following steps:

### 1. Database Initialization
- Establishes a connection with the RDS database.  
- Logs connection status and initializes SQLAlchemy session objects.  

### 2. Data Extraction
- Connects to **AWS S3** using `boto3`.  
- Fetches raw CSV files (e.g., `20250728 Open Electricity.csv`).  
- Reads data into a **pandas DataFrame** for processing.

### 3. Data Transformation
- Converts date fields into proper datetime objects.  
- Rounds all numeric columns to two decimal places.  
- Cleans and standardizes the dataset for consistency.  

### 4. Data Loading
- Maps each row to an `Electric` SQLAlchemy model instance.  
- Inserts all cleaned records into the RDS database in bulk.  
- Handles database connection errors gracefully and logs events for monitoring.

---

## 🧠 Key Python Components

| Function | Description |
|-----------|--------------|
| `database_initialization()` | Initializes and tests database connection |
| `extract()` | Downloads and reads CSV files from AWS S3 |
| `transform(data_frame)` | Cleans and formats raw data |
| `load(transformed_data, database_state)` | Loads processed data into the database |
| `create_object(row)` | Creates ORM objects for database insertion |

Each step is defined as an **Airflow task**, ensuring modularity and retry resilience.

---

## 📊 Data Visualization (Tableau)
After ETL completion, the processed dataset is visualized in **Tableau** to explore and communicate insights, such as:
- **Daily and monthly electricity generation trends**
- **Emission intensity (kgCO₂e/MWh) across energy sources**
- **Renewable vs non-renewable contribution over time**
- **Energy pricing dynamics**

The Tableau dashboards provide a clear and interactive view of the evolving energy landscape.

---



