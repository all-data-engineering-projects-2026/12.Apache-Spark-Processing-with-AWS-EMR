"""

Complete Command Reference: AWS EMR + Spark ETL Tutorial

1. S3 Bucket Setup

# Create logical folders in your existing bucket
aws s3api put-object --bucket emr-masterclass-bucket-01 --key scripts/ --region ap-south-1
aws s3api put-object --bucket emr-masterclass-bucket-01 --key input/   --region ap-south-1
aws s3api put-object --bucket emr-masterclass-bucket-01 --key output/  --region ap-south-1
aws s3api put-object --bucket emr-masterclass-bucket-01 --key emr-logs/ --region ap-south-1

# Upload Spark script
aws s3 cp spark-etl.py s3://emr-masterclass-bucket-01/scripts/ --region ap-south-1

# Upload input input_data
aws s3 cp ./input_data/ s3://emr-masterclass-bucket-01/input/ --recursive --region ap-south-1

2. Get EMR Cluster Information

# List active clusters
aws emr list-clusters --active --region ap-south-1

# Get specific cluster details (by name)
aws emr list-clusters \
  --active \
  --query "Clusters[?Name=='EMR Masterclass'].[Id, Name, Status]" \
  --output text \
  --region ap-south-1

# Get Instance Profile Role Name (for IAM fix)
aws emr describe-cluster \
  --cluster-id j-27FID2RA7818L \
  --query "Cluster.Ec2InstanceAttributes.IamInstanceProfile" \
  --output text \
  --region ap-south-1

3. Submit Spark Job (Final Working Version)
aws emr add-steps \
  --cluster-id j-27FID2RA7818L \
  --steps 'Type=Spark,Name="SparkETLJob-Fixed",ActionOnFailure=CONTINUE,Args=[--deploy-mode,cluster,--master,yarn,s3://emr-masterclass-bucket-01/scripts/spark-etl.py,s3://emr-masterclass-bucket-01/input/,s3://emr-masterclass-bucket-01/output/]' \
  --region ap-south-1


4. Monitoring Commands
Bash# Check status of a specific step
aws emr describe-step \
  --cluster-id j-27FID2RA7818L \
  --step-id s-09083302GP16WGX6ZZ9F \
  --region ap-south-1

# Check cluster state
aws emr describe-cluster \
  --cluster-id j-27FID2RA7818L \
  --query "Cluster.Status.State" \
  --output text \
  --region ap-south-1

# List all steps on the cluster
aws emr list-steps \
  --cluster-id j-27FID2RA7818L \
  --region ap-south-1

5. Checking Logs (When Job Fails)
# List log files for a step
aws s3 ls s3://aws-logs-<account_id>-ap-south-1/elasticmapreduce/j-27FID2RA7818L/steps/s-093707111JTFEAO72Y54/ --region ap-south-1

# View last 100 lines of stderr (most useful)
aws s3 cp s3://aws-logs-<account_id>-ap-south-1/elasticmapreduce/j-27FID2RA7818L/steps/s-093707111JTFEAO72Y54/stderr.gz - --region ap-south-1 | gunzip | tail -100

# Search for errors in logs
aws s3 cp s3://aws-logs-<account_id>-ap-south-1/elasticmapreduce/j-27FID2RA7818L/steps/s-093707111JTFEAO72Y54/stderr.gz - --region ap-south-1 | gunzip | grep -E "(Traceback|Error|Exception|Caused by)" | tail -50

6. IAM Permission Fix (S3 Access for EMR)
# Create S3 access policy
aws iam create-policy \
  --policy-name EMR-S3-Bucket-Access \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:ListBucket"],
            "Resource": "arn:aws:s3:::emr-masterclass-bucket-01"
        },
        {
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
            "Resource": "arn:aws:s3:::emr-masterclass-bucket-01/*"
        }
    ]
}' \
  --region ap-south-1

# Attach policy to EMR Instance Profile role
aws iam attach-role-policy \
  --role-name AmazonEMR-InstanceProfile-20260702T170928 \
  --policy-arn arn:aws:iam::<account_id>:policy/EMR-S3-Bucket-Access \
  --region ap-south-1

7. Verify Output
# List output folder
aws s3 ls s3://emr-masterclass-bucket-01/output/ --human-readable --region ap-south-1

# Full recursive view of bucket
aws s3 ls s3://emr-masterclass-bucket-01/ --recursive --human-readable --summarize --region ap-south-1

8. Terminate Cluster
Bash# Disable Termination Protection (if enabled)
aws emr modify-cluster-attributes \
  --cluster-id j-27FID2RA7818L \
  --no-termination-protected \
  --region ap-south-1

# Terminate the cluster
aws emr terminate-clusters \
  --cluster-ids j-27FID2RA7818L \
  --region ap-south-1

9. Optional Cleanup
# Delete EMR logs folder
aws s3 rm s3://emr-masterclass-bucket-01/emr-logs/ --recursive --region ap-south-1

"""