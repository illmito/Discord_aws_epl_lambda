import json
import boto3
import pandas as pd
import csv


def lambda_handler(event, context):
    url = 'https://www.football-data.co.uk/mmz4281/2223/E0.csv'
    table_name = 'Matches'

    csv_content = download_csv_from_url(url)
    csv_reader = csv.DictReader(csv_content.splitlines())
    data = []
    for row in csv_reader:
        data.append(row)
    write_to_dynamodb(table_name, data)

    return {
        'statusCode': 200,
        'body': 'Data imported to DynamoDB successfully.'
    }


def download_csv_from_url(url):
    df = pd.read_csv(url)
    df['Index'] = df['Date'] + ' - ' + df['HomeTeam']
    df.set_index('Index', inplace=True)
    df.drop(columns=[col for col in df.columns if col not in
                     ['Index',
                      'Date',
                      'HomeTeam',
                      'AwayTeam',
                      'FTHG',
                      'FTAG',
                      'FTR']], inplace=True)

    return df.to_csv(index=True)


def write_to_dynamodb(table_name, data):
    dynamodb = boto3.client('dynamodb')
    for item in data:
        index_value = item.pop('Index')
        item['Date-HomeTeam'] = {'S': index_value}
        item['Date'] = {'S': item['Date']}
        item['HomeTeam'] = {'S': item['HomeTeam']}
        item['AwayTeam'] = {'S': item['AwayTeam']}
        item['FTHG'] = {'N': item['FTHG']}
        item['FTAG'] = {'N': item['FTAG']}
        item['FTR'] = {'S': item['FTR']}
        dynamodb.put_item(TableName=table_name, Item=item)


def csv_to_dynamodb(event, context):
    url = 'https://www.football-data.co.uk/mmz4281/2223/E0.csv'
    table_name = 'Matches'

    csv_content = download_csv_from_url(url)
    csv_reader = csv.DictReader(csv_content.splitlines())
    data = []
    for row in csv_reader:
        data.append(row)
    write_to_dynamodb(table_name, data)

    return {
        'statusCode': 200,
        'body': 'Data imported to DynamoDB successfully.'
    }
