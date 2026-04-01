import logging
from typing import Any, Dict, Optional
from app.aws.boto_session import get_boto_session

logger = logging.getLogger(__name__)

class DynamoDBHelper:
    """Helper module to interface with AWS DynamoDB using Boto3"""
    
    def __init__(self):
        # Using the resource interface makes Dict interactions much simpler vs the raw client.
        self.session = get_boto_session()
        self.resource = self.session.resource("dynamodb")
        
    def put_item(self, table_name: str, item: Dict[str, Any]) -> bool:
        """
        Inserts or replaces an item in a DynamoDB table.
        Using the resource object automatically converts standard python dicts to Dynamo types.
        """
        try:
            table = self.resource.Table(table_name)
            table.put_item(Item=item)
            return True
        except Exception as e:
            logger.error(f"Failed to put item in DynamoDB ({table_name}): {str(e)}")
            return False
            
    def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single item from a DynamoDB table by its primary key.
        """
        try:
            table = self.resource.Table(table_name)
            response = table.get_item(Key=key)
            return response.get("Item")
        except Exception as e:
            logger.error(f"Failed to get item from DynamoDB ({table_name}): {str(e)}")
            return None
            
    def update_item_status(self, table_name: str, key: Dict[str, Any], status: str) -> bool:
        """
        Specific helper to quickly update a job's status field.
        """
        try:
            table = self.resource.Table(table_name)
            table.update_item(
                Key=key,
                UpdateExpression="set #status_col = :s",
                ExpressionAttributeNames={"#status_col": "status"},
                ExpressionAttributeValues={":s": status}
            )
            return True
        except Exception as e:
            logger.error(f"Failed to update status in DynamoDB ({table_name}): {str(e)}")
            return False
