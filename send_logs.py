import boto3
import time


def update_cloudwatch(transaction):
    AWS_REGION = "us-east-1"
    client = boto3.client('logs', region_name=AWS_REGION)
    describe_logs_streams = client.describe_log_streams(logGroupName='Bot-Processor')
    sequence_token = describe_logs_streams['logStreams'][0]
    log_event = {
        'logGroupName': 'Bot-Processor',
        'logStreamName': 'Logs-Processor',
        'logEvents': [
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': transaction
            },
        ],
    }

    if 'uploadSequenceToken' in sequence_token.keys():
        log_event['sequenceToken'] = sequence_token['uploadSequenceToken']
        response = client.put_log_events(**log_event)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Logs generated successfully")
        else:
            print("Logs generation failure")
    else:
        response = client.put_log_events(**log_event)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Logs generated successfully")
        else:
            print("Logs generation failure")

    #time.sleep(1)