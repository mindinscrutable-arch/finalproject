import os
import sys

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(__file__))

from app.aws.boto_session import get_boto_client
from app.core.config import settings

def test_s3():
    print(f"Testing S3 connection to bucket: {settings.S3_STORAGE_BUCKET} ...")
    s3 = get_boto_client('s3')
    try:
        s3.head_bucket(Bucket=settings.S3_STORAGE_BUCKET)
        print("SUCCESS: Successfully connected to S3 Bucket!")
    except Exception as e:
        print(f"ERROR: S3 Error: {e}")

def test_dynamodb():
    print(f"\nTesting DynamoDB connection to table: {settings.DYNAMODB_JOBS_TABLE} ...")
    dynamodb = get_boto_client('dynamodb')
    try:
        dynamodb.describe_table(TableName=settings.DYNAMODB_JOBS_TABLE)
        print("SUCCESS: Successfully connected to DynamoDB Table!")
    except Exception as e:
        print(f"ERROR: DynamoDB Error: {e}")

if __name__ == "__main__":
    if not settings.AWS_STORAGE_ENABLED:
        print("AWS Storage is currently disabled in .env (AWS_STORAGE_ENABLED=false)")
    else:
        test_s3()
        test_dynamodb()
