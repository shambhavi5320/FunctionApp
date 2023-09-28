import azure.functions as func
import logging
import csv
from io import StringIO
from datetime import datetime, timedelta
from transformations import actual, accrual 

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="transform-actual", methods=["POST"])
def transform_actual(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Transform function processed a request.')

    try:
        req_body = req.get_body().decode("utf-8")
    except ValueError:
        return func.HttpResponse("Invalid request body", status_code=400)

    payload = []

    csv_reader = csv.DictReader(StringIO(req_body))
    for row in csv_reader:
        payload.append(row)

    transformed_payload = [actual.transform_actual(record) for record in payload]

    return func.HttpResponse(str(transformed_payload), status_code=200, mimetype="application/json")


@app.route(route="transform-accrual", methods=["POST"])
def transform_accrual(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Transform accrual function processed a request.')

    try:
        req_body = req.get_body().decode("utf-8")
    except ValueError:
        return func.HttpResponse("Invalid request body", status_code=400)

    payload = []

    csv_reader = csv.DictReader(StringIO(req_body))
    for row in csv_reader:
        payload.append(row)

    transformed_payload = [accrual.transform_accrual(record) for record in payload]

    return func.HttpResponse(str(transformed_payload), status_code=200, mimetype="application/json")
