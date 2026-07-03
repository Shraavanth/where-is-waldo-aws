import json
import boto3
import datetime
from boto3.dynamodb.conditions import Key

# -----------------------
# DynamoDB Setup
# -----------------------

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PlayerScores')

# -----------------------
# Coordinates
# -----------------------

coordinates = {

    "The Beach.jpeg": {
        "Waldo": {
            "xmin": 582,
            "xmax": 624,
            "ymin": 384,
            "ymax": 453
        }
    },

    "The market.jpeg": {
        "Wenda": {
            "xmin": 579,
            "xmax": 626,
            "ymin": 278,
            "ymax": 354
        }
    },

    "The Medieval City.jpeg": {
        "Odlaw": {
            "xmin": 14,
            "xmax": 84,
            "ymin": 1149,
            "ymax": 1273
        }
    }

}

# -----------------------
# Save Score
# -----------------------

def save_score(player_id, score, level, time_taken):

    table.put_item(
        Item={
            'PlayerID': player_id,
            'Score': int(score),
            'GameID': 'WaldoGame v1',
            'Level': int(level),
            'TimeTaken': int(time_taken),
            'Date': str(datetime.date.today())
        }
    )

# -----------------------
# Leaderboard
# -----------------------

def get_leaderboard():

    response = table.query(

        IndexName='GameID-Score-index',

        KeyConditionExpression=
        Key('GameID').eq('WaldoGame v1'),

        ScanIndexForward=False,

        Limit=5
    )

    return response['Items']

# -----------------------
# Main Lambda Function
# -----------------------

def lambda_handler(event, context):

    if "body" in event:
        event = json.loads(event["body"])

    image = event["image"]
    character = event["character"]

    x = event["x"]
    y = event["y"]

    player_id = event.get("player_id", "guest")

    target = coordinates[image][character]

    if (target["xmin"] <= x <= target["xmax"] and
            target["ymin"] <= y <= target["ymax"]):

        return {
            "statusCode": 200,

            "headers": {
                "Access-Control-Allow-Origin": "*"
            },

            "body": json.dumps({

                "result": "Correct!",
                "score": 10

            })
        }

    return {

        "statusCode": 200,

        "headers": {
            "Access-Control-Allow-Origin": "*"
        },

        "body": json.dumps({

            "result": "Wrong!",
            "score": 0

        })
    }