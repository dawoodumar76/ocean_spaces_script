import argparse
import os
import json
from urllib.parse import urlparse
import boto3
from botocore.client import Config
from dotenv import load_dotenv
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# You can load these credentials from environment variables or set them here directly
SPACES_ACCESS_KEY_ID = os.getenv('SPACES_ACCESS_KEY_ID')
SPACES_SECRET_ACCESS_KEY = os.getenv('SPACES_SECRET_ACCESS_KEY')

def get_do_spaces_details(url):
    """
    Extracts region, bucket name, and object key from a DigitalOcean Spaces URL.
    
    URL format: https://<bucket-name>.<region>.digitaloceanspaces.com/<object-key>
    """
    parsed_url = urlparse(url)
    bucket_name, region = parsed_url.netloc.split('.')[0], parsed_url.netloc.split('.')[1]
    object_key = parsed_url.path.lstrip('/')
    return bucket_name, region, object_key

def upload_file_to_space(file_path, bucket_url):
    """
    Uploads a file to a DigitalOcean Space.
    """
    bucket_name, region, _ = get_do_spaces_details(bucket_url)
    endpoint_url = f'https://{region}.digitaloceanspaces.com'

    s3_client = boto3.client(
        's3',
        region_name=region,
        endpoint_url=endpoint_url,
        aws_access_key_id=SPACES_ACCESS_KEY_ID,
        aws_secret_access_key=SPACES_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )

    object_name = os.path.basename(file_path)

    # Upload the file
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        logging.info(f"File {file_path} uploaded successfully as {object_name} to bucket {bucket_name}")
    except Exception as e:
        logging.error(f"Failed to upload file {file_path}: {e}")

def list_items_in_space(bucket_url):
    """
    Lists all items in a DigitalOcean Space bucket.
    """
    bucket_name, region, _ = get_do_spaces_details(bucket_url)
    endpoint_url = f'https://{region}.digitaloceanspaces.com'

    s3_client = boto3.client(
        's3',
        region_name=region,
        endpoint_url=endpoint_url,
        aws_access_key_id=SPACES_ACCESS_KEY_ID,
        aws_secret_access_key=SPACES_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )

    # List objects in the bucket
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            logging.info(f"Files in {bucket_name}:")
            for obj in response['Contents']:
                logging.info(f"  - {obj['Key']}")
        else:
            logging.info(f"No files found in bucket {bucket_name}")
    except Exception as e:
        logging.error(f"Failed to list items in bucket {bucket_name}: {e}")

def delete_file_from_url(url):
    """
    Deletes a file from DigitalOcean Space using the details from the URL.
    """
    bucket_name, region, object_key = get_do_spaces_details(url)

    endpoint_url = f'https://{region}.digitaloceanspaces.com'

    s3_client = boto3.client(
        's3',
        region_name=region,
        endpoint_url=endpoint_url,
        aws_access_key_id=SPACES_ACCESS_KEY_ID,
        aws_secret_access_key=SPACES_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )

    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        logging.info(f"File {object_key} deleted successfully from bucket {bucket_name}")
    except Exception as e:
        logging.error(f"Failed to delete file {object_key}: {e}")

def main(action, bucket_url=None, file_path=None, urls=None):
    """
    Performs the specified action (upload, list, delete) on the DigitalOcean Space.
    """
    if action == 'upload' and file_path:
        upload_file_to_space(file_path, bucket_url)
    
    elif action == 'list' and bucket_url:
        list_items_in_space(bucket_url)

    elif action == 'delete' and urls:
        urls_list = json.loads(urls)
        for url in urls_list:
            logging.info(f"Deleting file from URL: {url}")
            delete_file_from_url(url)
    
    else:
        logging.error("Invalid action or missing arguments")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage files in DigitalOcean Spaces (upload, list, delete).')
    parser.add_argument('action', choices=['upload', 'list', 'delete'], help='Action to perform: upload, list, or delete')
    parser.add_argument('--bucket-url', help='The DigitalOcean Spaces bucket URL (required for upload and list)')
    parser.add_argument('--file-path', help='File to upload to the space (required for upload)')
    parser.add_argument('--urls', help='JSON-encoded list of URLs to delete (required for delete)')
    args = parser.parse_args()

    main(args.action, args.bucket_url, args.file_path, args.urls)
