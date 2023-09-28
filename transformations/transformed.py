def transform_payload(headers, input_payload):
    transformed_payload = []

    for row in input_payload:
        transformed_row = {}
        for col in headers:
            try:
                transformed_row[col] = row.get(col, None)
            except ValueError:
                transformed_row[col] = None
        transformed_payload.append(transformed_row)

    return transformed_payload