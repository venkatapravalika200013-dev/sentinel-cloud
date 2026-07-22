import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# Configuration & Initialization
DRY_RUN = os.getenv("DRY_RUN", "True").lower() == "true"
ENDPOINT_URL = "http://localhost:4566"

s3 = boto3.client(
    's3',
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    config=Config(s3={'addressing_style': 'path'})
)

def scan_and_remediate():
    print("=" * 60)
    print(f"🤖 SENTINEL-CLOUD GOVERNANCE ENGINE | Mode: {'🛡️ DRY-RUN' if DRY_RUN else '💥 LIVE-EXECUTION'}")
    print("=" * 60)

    response = s3.list_buckets()
    buckets = response.get('Buckets', [])

    if not buckets:
        print("No buckets found in environment.")
        return

    for bucket in buckets:
        name = bucket['Name']
        try:
            tagging = s3.get_bucket_tagging(Bucket=name)
            tags = {t['Key']: t['Value'] for t in tagging.get('TagSet', [])}

            if 'Project' in tags:
                print(f"✅ COMPLIANT: Bucket '{name}' [Tag: Project={tags['Project']}]")
            else:
                handle_non_compliant_bucket(name, reason="Missing mandatory 'Project' tag")

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchTagSet':
                handle_non_compliant_bucket(name, reason="No tags present on resource")
            else:
                print(f"❓ ERROR scanning '{name}': {e}")

def handle_non_compliant_bucket(name, reason):
    print(f"🚨 NON-COMPLIANT RESOURCE: '{name}' | Reason: {reason}")

    if DRY_RUN:
        print(f"   🛡️ [DRY RUN] Resource flagged for deletion. No action taken.")
    else:
        print(f"   💥 ACTION: Initiating termination for '{name}'...")
        try:
            s3.delete_bucket(Bucket=name)
            verify_deletion(name)
        except ClientError as err:
            print(f"   ❌ FAILED to delete '{name}': {err}")

def verify_deletion(name):
    try:
        s3.head_bucket(Bucket=name)
        print(f"   ⚠️ WARNING: Bucket '{name}' still exists after deletion call.")
    except ClientError:
        print(f"   ✅ 100% CONFIRMED: Bucket '{name}' has been removed from the cloud.")

if __name__ == "__main__":
    scan_and_remediate()
