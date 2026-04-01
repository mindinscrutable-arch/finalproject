import json
import logging
from typing import Any, Dict, Optional
from app.aws.boto_session import get_boto_client

logger = logging.getLogger(__name__)

class S3Helper:
    """Helper module to interface with AWS S3 using Boto3"""
    
    def __init__(self):
        # We reuse the configured client generator from Person C's boto_session.py
        self.client = get_boto_client("s3")
        
    def upload_json(self, bucket_name: str, object_key: str, data: Dict[str, Any]) -> bool:
        """Uploads a dictionary as a JSON file to S3"""
        try:
            json_data = json.dumps(data, indent=2)
            self.client.put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=json_data,
                ContentType="application/json"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to upload JSON to S3 ({bucket_name}/{object_key}): {str(e)}")
            return False
            
    def download_json(self, bucket_name: str, object_key: str) -> Optional[Dict[str, Any]]:
        """Downloads a JSON file from S3 and parses it to a dict"""
        try:
            response = self.client.get_object(Bucket=bucket_name, Key=object_key)
            content = response['Body'].read().decode('utf-8')
            return json.loads(content)
        except Exception as e:
            logger.error(f"Failed to download JSON from S3 ({bucket_name}/{object_key}): {str(e)}")
            return None
