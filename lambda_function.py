import json
import boto3

s3 = boto3.client("s3")
glue = boto3.client("glue")

def lambda_handler(event, context):
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    obj = s3.get_object(Bucket=bucket, Key=key)
    payload = json.loads(obj["Body"].read())

    process_date = payload["process_date"]

    glue.start_job_run(
        JobName="etl_b3_refined",
        Arguments={
            "--PROCESS_DATE": process_date
        }
    )
