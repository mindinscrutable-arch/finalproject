import os
import sys

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(__file__))

from app.aws.boto_session import get_boto_client
from app.core.config import settings

def check_dynamodb_items():
    print(f"Scanning DynamoDB Table: {settings.DYNAMODB_JOBS_TABLE} ...\n")
    dynamodb = get_boto_client('dynamodb')
    
    try:
        response = dynamodb.scan(TableName=settings.DYNAMODB_JOBS_TABLE, Limit=5)
        items = response.get('Items', [])
        
        if not items:
            print("The table is empty. No jobs found.")
            return

        print(f"SUCCESS: Found {len(items)} item(s) in the table! Here is the latest data:\n")
        
        for item in items:
            # DynamoDB returns items in a typed dict format like {"job_id": {"S": "123..."}, "status": {"S": "COMPLETED"}}
            # We can print it directly
            print("-" * 40)
            for key, val_dict in item.items():
                # Extract the actual value from the DynamoDB type wrapper
                val = list(val_dict.values())[0]
                print(f"{key}: {val}")
            
    except Exception as e:
        print(f"ERROR: Error scanning DynamoDB Table: {e}")

if __name__ == "__main__":
    check_dynamodb_items()
