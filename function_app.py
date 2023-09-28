import azure.functions as func
import logging
import csv
import json
from io import StringIO
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from transformations import actual, accrual, accountSchedule, transformed, xml_to_json

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

@app.route(route="combined_transformation", methods=["POST"])
def combined_transformation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Transform accrual function processed a request.')

    try:
        req_body = req.get_body().decode("utf-8")
    except ValueError:
        return func.HttpResponse("Invalid request body", status_code=400)

    payload = []

    csv_reader = csv.DictReader(StringIO(req_body))
    
    next(csv_reader)
    
    for row in csv_reader:
        payload.append(row)

    transformed_payload = [accrual.combined_transformation(payload_row) for payload_row in payload]

    return func.HttpResponse(str(transformed_payload), status_code=200, mimetype="application/json")

@app.route(route="transform_account_schedule", methods=["POST"])
def transform_account_schedule(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Account Schedule transformation function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid request body", status_code=400)

    company = req_body.get("company", "Talking Rain")
    input_payload = req_body.get("payload", [])

    csv_output = accountSchedule.transform_account_schedule(company, input_payload)

    return func.HttpResponse(
        csv_output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=output.csv"}
    )

@app.route(route="transform_dataweave", methods=["POST"])
def transform_dataweave(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('DataWeave-like transformation function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid request body", status_code=400)

    headers = req_body.get("headers", [])
    data = req_body.get("data", [])

    payload = []

    if not headers or not data:
        return func.HttpResponse("Invalid input data format", status_code=400)

    csv_data = "\n".join(",".join(row) for row in data)
    csv_rows = csv_data.strip().split("\n")
    csv_reader = csv.reader(StringIO("\n".join(csv_rows)))

    for row_index, row in enumerate(csv_reader):
        if row_index == 0:
            # If it's the first row, map the columns based on their positions
            col_mapping = {col_index: col for col_index, col in enumerate(row)}
        else:
            # For data rows, use the mapping to create a dictionary
            transformed_row = {headers[col_index]: value for col_index, value in col_mapping.items()}
            payload.append(transformed_row)

    transformed_payload = transformed.transform_payload(headers, payload)  # Pass headers and input_payload

    return func.HttpResponse(
        json.dumps(transformed_payload),
        status_code=200,
        mimetype="application/json"
    )

@app.route(route="transform_csv_for_dataweave", methods=["POST"])
def transform_csv_for_dataweave(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_body().decode("utf-8")
    except ValueError:
        return func.HttpResponse("Invalid request body", status_code=400)

    lines = req_body.strip().split('\n')
    header = lines[0].split(',')
    data_rows = [line.split(',') for line in lines[1:]]

    payload = {
        "headers": header,
        "data": data_rows
    }

    json_payload = json.dumps(payload)

    return func.HttpResponse(json_payload, status_code=200, mimetype="application/json")

@app.route(route="transform_xml_to_json", methods=["POST"])
def transform_xml_to_json(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Transform XML to JSON function processed a request.')

    try:
        xml_data = req.get_body().decode("utf-8")
    except ValueError:
        return func.HttpResponse("Invalid request body", status_code=400)

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        return func.HttpResponse(f"Error parsing XML: {str(e)}", status_code=400)
    
    json_data = json.dumps(xml_to_json.xml_to_dict(root), indent=2)
    

    return func.HttpResponse(json_data, status_code=200, mimetype="application/json")