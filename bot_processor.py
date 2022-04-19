import logging
from botocore.exceptions import ClientError
from datetime import date
import upload_data_s3
import time
import csv
import json
import boto3

from send_logs import update_cloudwatch



class BotProcessor:
    """The 'SQS AWS' client subscribes to the 'SNS AWS' topic. 
    This class is responsible for processing the information it receives, 
    taking only the data that is needed and redirecting it"""

    date = date.today()
    def sqs_reader(self):
        """Receives transactional data and processes it, 
        returning a list with specific values corresponding to each transaction performed.
        It also removes the message from 'SQS AWS' once it has been processed"""
        logging.info(f'<Start> - <SQS.receive_messsage()> {BotProcessor.date}')
        sqs_client = boto3.client("sqs")
        transactions = []
        while True:
            response = sqs_client.receive_message(
                QueueUrl="https://sqs.us-east-1.amazonaws.com/360729631529/SQS-EMA",
                AttributeNames=['All'],
                MaxNumberOfMessages=1
            )
            try:
                message = response['Messages'][0]
                receipt_handle = message['ReceiptHandle']
                message_body = json.loads(message['Body'])
                data_tx = message_body['Message']
                update_cloudwatch("Mensaje leido de SQS >> " + str(data_tx))
                transactions.append(json.loads(data_tx))
            except KeyError:
                break
    
            try:
                resp = sqs_client.delete_message(
                    QueueUrl= "https://sqs.us-east-1.amazonaws.com/360729631529/SQS-EMA", 
                    ReceiptHandle= receipt_handle
                )
                if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print("Mensaje eliminado con éxito..")
                    logging.info('Mensaje eliminado de cola SQS.. ReceiptHandle: ' + str(receipt_handle))
                    update_cloudwatch("< Mensaje eliminado de SQS >")
            except ClientError as e:
                logging.error(e)
                return False          
        return transactions
        
    def writer_csv_file_and_upload(self):
        """Function in charge of creating and writing files in 'csv' format. 
        This file will contain all the daily transactional information of the token"""

        fieldnames = [
                'blockHash', 
                'blockNumber', 
                'from', 
                'gas', 
                'gasPrice', 
                'maxFeePerGas', 
                'maxPriorityFeePerGas', 
                'hash', 
                'input', 
                'nonce', 
                'to', 
                'transactionIndex', 
                'value', 
                'type', 
                'accessList', 
                'chainId', 
                'v', 
                'r', 
                's' 
        ]
        
        data_tx = self.sqs_reader()
        path_file = f'csvFiles/transactions-{BotProcessor.date}.csv'
        with open(path_file, 'w', encoding='UTF8', newline='') as data:
            writer = csv.DictWriter(data, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_tx)
        upload_data_s3.upload_file(path_file, "s3-tx")
        return True

if __name__ == '__main__':
    logging.basicConfig(filename='proccesedData_loggs.log', format='%(levelname)s:%(message)s', level=logging.INFO)
    bot= BotProcessor()
    while True:
        try:
            bot.writer_csv_file_and_upload()
            print("--------------------------")
            time.sleep(3300)
        except Exception as e:
            print("< Bot-Processor stoped >")
            print(e)
    