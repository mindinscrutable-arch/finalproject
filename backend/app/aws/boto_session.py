import boto3
from botocore.config import Config
from app.core.config import settings

def get_boto_session() -> boto3.Session:
    """
    Creates and returns a configured Boto3 session.
    It uses the AWS_PROFILE and AWS_REGION from settings if provided.
    """
    kwargs = {}
    if settings.AWS_PROFILE:
        kwargs["profile_name"] = settings.AWS_PROFILE
    if settings.AWS_REGION:
        kwargs["region_name"] = settings.AWS_REGION

    return boto3.Session(**kwargs)

def get_boto_client(service_name: str, **kwargs) -> boto3.client:
    """
    Returns a Boto3 client for the specified service name.
    """
    session = get_boto_session()
    
    # Configure retry behavior
    boto_config = Config(
        retries=dict(
            max_attempts=3
        )
    )
    
    return session.client(
        service_name=service_name,
        config=boto_config,
        **kwargs
    )
