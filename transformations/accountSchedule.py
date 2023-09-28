def transform_account_schedule(company, input_payload):
    output_payload = []
    for item in input_payload:
        transformed_item = {
            "ID": f"{item.get('Schedule_Name', '')}-{item.get('Line_No', '')}-BIC" if company != "Talking Rain" else f"{item.get('Schedule_Name', '')}-{item.get('Line_No', '')}",
            "Company": company,
            "Schedule Name": item.get("Schedule_Name", ""),
            "Line No.": item.get("Line_No", ""),
            "Row No.": item.get("Row_No", ""),
            "Description": item.get("Description", "").replace(",", ""),
            "Totaling": item.get("Totaling", ""),
            "Totaling Type": item.get("Totaling_Type", ""),
            "New Page": str(item.get("New_Page", False)).lower(),
            "Show": str(item.get("Show", False)).lower(),
            "Dimension 1 Totaling": item.get("Dimension_1_Totaling", ""),
            "Dimension 2 Totaling": item.get("Dimension_2_Totaling", ""),
            "Dimension 3 Totaling": item.get("Dimension_3_Totaling", ""),
            "Dimension 4 Totaling": item.get("Dimension_4_Totaling", ""),
            "Bold": str(item.get("Bold", False)).lower(),
            "Italic": str(item.get("Italic", False)).lower(),
            "Underline": str(item.get("Underline", False)).lower(),
            "Show Opposite Sign": str(item.get("Show_Opposite_Sign", False)).lower(),
            "Row Type": item.get("Row_Type", ""),
            "Amount Type": item.get("Amount_Type", ""),
            "Double Underline": str(item.get("Double_Underline", False)).lower(),
            "Cost Center Totaling": item.get("Cost_Center_Totaling", ""),
            "Cost Object Totaling": item.get("Cost_Object_Totaling", "")
        }
        output_payload.append(transformed_item)
    
    # Format the output_payload as CSV rows
    csv_output = "ID,Company,Schedule Name,Line No.,Row No.,Description,Totaling,Totaling Type,New Page,Show,Dimension 1 Totaling,Dimension 2 Totaling,Dimension 3 Totaling,Dimension 4 Totaling,Bold,Italic,Underline,Show Opposite Sign,Row Type,Amount Type,Double Underline,Cost Center Totaling,Cost Object Totaling\n"
    for item in output_payload:
        row_values = [
            item["ID"],
            item["Company"],
            item["Schedule Name"],
            item["Line No."],
            item["Row No."],
            item["Description"],
            item["Totaling"],
            item["Totaling Type"],
            item["New Page"],
            item["Show"],
            item["Dimension 1 Totaling"],
            item["Dimension 2 Totaling"],
            item["Dimension 3 Totaling"],
            item["Dimension 4 Totaling"],
            item["Bold"],
            item["Italic"],
            item["Underline"],
            item["Show Opposite Sign"],
            item["Row Type"],
            item["Amount Type"],
            item["Double Underline"],
            item["Cost Center Totaling"],
            item["Cost Object Totaling"]
        ]
        csv_output += ",".join([f'"{value}"' for value in row_values]) + "\n"

    return csv_output
