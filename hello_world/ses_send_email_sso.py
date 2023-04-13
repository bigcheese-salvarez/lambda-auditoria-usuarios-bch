
def lambda_handler(event, context):
    RECIPIENTS = ["tito", "tito2", "chicho", "lolo"]
    for RECIPIENT in RECIPIENTS:
        print(RECIPIENT)