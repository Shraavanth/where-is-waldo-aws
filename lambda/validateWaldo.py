import json


def lambda_handler(event, context):

    try:

        # Handle API Gateway requests
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        x = body["x"]
        y = body["y"]

        # Waldo location
        X_MIN = 250
        X_MAX = 300
        Y_MIN = 150
        Y_MAX = 200

        if X_MIN <= x <= X_MAX and Y_MIN <= y <= Y_MAX:

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
                "result": "Wrong Location",
                "score": 0
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }