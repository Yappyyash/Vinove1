import boto3
import os
from botocore.exceptions import NoCredentialsError

# AWS S3 Configuration
S3_BUCKET_NAME = 'shailenderproject'
S3_ACCESS_KEY = 'AKIA2RSH2FF2Z55GNVGB'
S3_SECRET_KEY = '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'
LOCAL_DIRECTORY = 'C:/Users/UNITECH/Desktop/Vinove/vinove/media/'

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)

def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket and delete the file locally if successful."""
    if object_name is None:
        object_name = os.path.basename(file_name)
    
    try:
        # Upload the file
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Uploaded {file_name} to {bucket}/{object_name}")
        
        # If upload was successful, delete the file locally
        os.remove(file_name)
        print(f"Deleted {file_name} from local storage")
        
        
    except FileNotFoundError:
        print(f"The file {file_name} was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Failed to upload {file_name} to S3: {e}")

def upload_images_in_directory(directory, bucket):
    """Upload all images in the directory to the specified S3 bucket."""
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.svg', '.webp')):
            file_path = os.path.join(directory, filename)
            upload_to_s3(file_path, bucket)

if __name__ == "__main__":
    upload_images_in_directory(LOCAL_DIRECTORY, S3_BUCKET_NAME)
