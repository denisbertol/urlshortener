import uuid
import logging

import boto3

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
      
def lambda_handler(event, context):
    # Parse targetUrl
    fullUrl = event['fullUrl']

    ssm = boto3.client('ssm')

    parameter = ssm.get_parameter(Name='/app/prod/urlshortener/baseUrl', WithDecryption=True)

    baseUrl = parameter ['Parameter']['Value']

    # Create a unique id (take first 8 chars)
    id = str(uuid.uuid4())[0:8]

    client = boto3.client('dynamodb')
    data = client.put_item(
    TableName='tb_urls',
    Item={
      'urlcurta': {
        'S': '' + str(id)
      },
      'urlcompleta': {
        'S': '' + str(fullUrl)
      }
    }
  )

    # Create the redirect URL
    url = baseUrl + id

    return {
        'shortUrl': '%s' % url,'fullUrl': '%s' % fullUrl
    }
