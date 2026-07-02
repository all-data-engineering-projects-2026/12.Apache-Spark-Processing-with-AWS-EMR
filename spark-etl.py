import sys
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: spark-etl.py <input-folder> <output-folder>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    spark = SparkSession.builder.appName("SparkETL").getOrCreate()

    # Read CSV
    df = spark.read.option("inferSchema", "true") \
                    .option("header", "true") \
                    .csv(input_path)

    # Add current timestamp column
    df_with_date = df.withColumn("current_date", lit(datetime.now()))

    # Show schema and sample (only for debugging - remove in production)
    df_with_date.printSchema()
    df_with_date.show(5, truncate=False)

    print(f"Total number of records: {df_with_date.count()}")

    # Write as Parquet
    df_with_date.write.mode("overwrite").parquet(output_path)

    print("Job completed successfully!")
    spark.stop()