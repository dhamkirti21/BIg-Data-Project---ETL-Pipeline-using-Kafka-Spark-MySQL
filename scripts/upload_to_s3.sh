#!/bin/bash

set -e  # fail fast

LOCAL_PARQUET_DIR="/home/talentum/CCEE_BigDataProject/output"
S3_BUCKET="s3://ccee-bigdata-project/data"

echo "Uploading parquet files to S3..."
aws s3 sync "$LOCAL_PARQUET_DIR" "$S3_BUCKET"

echo "S3 upload completed successfully"
