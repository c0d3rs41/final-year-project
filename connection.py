import sys
import boto3
import os

# AWS credentials
ACCESS_KEY = "Your-access-key"
SECRET_ACCESS_KEY = "Your-secret-access-key"

# S3 bucket name
BUCKET_NAME = "Your-bucket-name"

def upload_to_s3(local_file_path, bucket_name):
    try:
        # Create an S3 client
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)

        # Extract file name from the local file path
        file_name = os.path.basename(local_file_path)

        # Upload file to S3
        s3.upload_file(local_file_path, bucket_name, file_name)
        print(f"File uploaded successfully to {bucket_name}")

    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <local_file_path>")
    else:
        LOCAL_FILE_PATH = sys.argv[1]
        upload_to_s3(LOCAL_FILE_PATH, BUCKET_NAME)