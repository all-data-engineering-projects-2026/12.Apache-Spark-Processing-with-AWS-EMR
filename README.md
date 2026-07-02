# AWS EMR Data Processing for Data Engineers

> **End-to-End Spark ETL Pipeline on Amazon EMR**

[![EMR](https://img.shields.io/badge/Amazon%20EMR-Spark-orange?logo=amazonaws)](https://aws.amazon.com/emr/)
[![Spark](https://img.shields.io/badge/Apache%20Spark-PySpark-orange?logo=apachespark)](https://spark.apache.org/)
[![AWS](https://img.shields.io/badge/AWS-CLI%20%7C%20S3-FF9900?logo=amazonaws)](https://aws.amazon.com/)

---

## 📌 Project Overview

This project demonstrates how to build and run a **production-grade Spark ETL pipeline** on **Amazon EMR** (Elastic MapReduce). It covers the complete workflow from cluster setup to job submission, monitoring, IAM troubleshooting, and output verification.

### What It Does

- Reads CSV data from S3
- Performs simple transformations using PySpark (adds processing timestamp)
- Writes output as **Parquet** format to S3
- Runs on a managed **Amazon EMR** cluster
- Includes complete AWS CLI automation and troubleshooting guide

---

## 🏛️ Architecture

```
                    ┌─────────────────────┐
                    │   Input CSV Files   │
                    │   (S3: input/)      │
                    └──────────┬──────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────┐
│              Amazon EMR Cluster                    │
│         (Apache Spark on YARN)                     │
│                                                    │
│   spark-etl.py                                     │
│   ├── Read CSV from S3                             │
│   ├── Add current_date column                      │
│   └── other transaformation etc....                │
│   └── Write Parquet to S3 (output/)                │
└────────────────────────────┬───────────────────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │   Output Parquet    │
                    │   (S3: output/)     │
                    └─────────────────────┘
```

**Orchestration:** AWS CLI (`aws emr add-steps`)

---

## 🛠️ Technology Stack

| Component            | Technology                    | Purpose |
|----------------------|-------------------------------|--------|
| **Big Data Engine**  | Apache Spark (PySpark)        | ETL processing |
| **Cluster**          | Amazon EMR                    | Managed Spark/Hadoop cluster |
| **Storage**          | Amazon S3                     | Input, scripts, output, logs |
| **Job Submission**   | AWS CLI (`emr add-steps`)     | Submit and manage Spark jobs |
| **Security**         | IAM Roles & Policies          | EMR Instance Profile + S3 access |
| **Monitoring**       | EMR Step Logs                 | Debugging and status tracking |

---

## 📁 Project Structure

```
12.EMR-for-data-engineers/
├── spark-etl.py              # Main PySpark ETL script
├── commands.py               # Complete AWS CLI reference (setup, submit, monitor, IAM fix)
├── input_data/
│   └── tripdata.csv          # Sample green taxi dataset
├── README.md
└── .gitignore
```

---

## 🚀 How to Use

### 1. Prepare S3 Bucket

```bash
# Create folders
aws s3api put-object --bucket YOUR_BUCKET --key scripts/
aws s3api put-object --bucket YOUR_BUCKET --key input/
aws s3api put-object --bucket YOUR_BUCKET --key output/

# Upload script and data
aws s3 cp spark-etl.py s3://YOUR_BUCKET/scripts/
aws s3 cp ./data/ s3://YOUR_BUCKET/input/ --recursive
```

### 2. Create EMR Cluster

Create an EMR cluster via AWS Console or CLI with Spark installed.

### 3. Submit Spark Job

```bash
aws emr add-steps \
  --cluster-id j-XXXXXXXXXXXXX \
  --steps 'Type=Spark,Name="SparkETLJob",ActionOnFailure=CONTINUE,Args=[--deploy-mode,cluster,--master,yarn,s3://YOUR_BUCKET/scripts/spark-etl.py,s3://YOUR_BUCKET/input/,s3://YOUR_BUCKET/output/]' \
  --region ap-south-1
```

### 4. Monitor Job

```bash
# Check step status
aws emr describe-step --cluster-id j-XXXXXXXXXXXXX --step-id s-XXXXXXXXXXXXX

# View logs (most useful)
aws s3 cp s3://aws-logs-ACCOUNT-ap-south-1/elasticmapreduce/j-XXXXXXXXXXXXX/steps/s-XXXXXXXXXXXXX/stderr.gz - | gunzip | tail -100
```

### 5. Fix Common IAM Issue

If the job fails with S3 access errors, attach a custom S3 policy to the EMR Instance Profile role (see `commands.py` for exact policy).

### 6. Verify Output

```bash
aws s3 ls s3://YOUR_BUCKET/output/ --human-readable
```

---

## ✅ Key Features

- Simple but complete **Spark ETL** example on EMR
- **Production-ready** command reference (`commands.py`)
- Covers **IAM permission fixes** (most common EMR issue)
- Includes **monitoring and debugging** commands
- Clean separation between script and infrastructure commands

---

## 🧠 Skills Demonstrated

- Amazon EMR cluster management
- Apache Spark (PySpark) development for ETL
- Running Spark jobs on YARN in cluster mode
- AWS CLI automation for big data workloads
- S3 + EMR integration best practices
- IAM troubleshooting for EMR
- Job monitoring and log analysis on EMR
- End-to-end cloud data pipeline implementation

---

## 📄 Documentation

| File                                 | Description |
|--------------------------------------|-------------|
| `AWS_EMR_Data_Engineering_Notes.pdf` | Complete technical documentation with implementation details |
| `README_AWS_EMR_Data_Engineering.md` | This file |
| `commands.py`                        | Full command reference for EMR operations |

---

## 👨‍💻 Author

**Himanshu**  
Data Engineering | AWS | Spark | Airflow | Modern Data Platforms

---

*This project is ideal for demonstrating practical experience with Amazon EMR and Spark on AWS for Data Engineer roles.*