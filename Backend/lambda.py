import json
import boto3
import time

# AWS Clients
textract = boto3.client('textract')
s3 = boto3.client('s3')

def lambda_handler(event, context):

    try:

        # Get bucket and uploaded file dynamically
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print("Bucket:", bucket)
        print("Uploaded File:", key)

        # Start Textract async job
        response = textract.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            }
        )

        job_id = response['JobId']

        print("Job ID:", job_id)

        # Wait for Textract completion
        while True:

            result = textract.get_document_text_detection(
                JobId=job_id
            )

            status = result['JobStatus']

            print("Current Status:", status)

            if status == 'SUCCEEDED':
                break

            elif status == 'FAILED':
                raise Exception("Textract Processing Failed")

            time.sleep(5)

        extracted_text = ""

        next_token = None

        # Read all extracted pages
        while True:

            if next_token:

                result = textract.get_document_text_detection(
                    JobId=job_id,
                    NextToken=next_token
                )

            else:

                result = textract.get_document_text_detection(
                    JobId=job_id
                )

            # Extract text
            for block in result['Blocks']:

                if block['BlockType'] == 'LINE':

                    extracted_text += block['Text'] + "\n"

            next_token = result.get('NextToken')

            if not next_token:
                break

        print("Extracted Text:")
        print(extracted_text)

        # Create TXT result filename
        result_file = key.replace(".pdf", ".txt")

        # Store extracted text in S3
        s3.put_object(
            Bucket=bucket,
            Key="results/" + result_file,
            Body=extracted_text
        )

        print("Result stored in S3 successfully")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'PDF processed successfully',
                'result_file': "results/" + result_file
            })
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
