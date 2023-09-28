from datetime import datetime, timedelta

def transform_actual(record):
    specialAccounts = ["10300", "10310", "11220", "21040", "21100", "21150", "22320", "22340"]
    fileMonth = "004"
    
    def getAmount(rec):
        return str(-1 * float(rec.get("Credit Amount")) + float(rec.get("Debit Amount")))
    
    mule_posting_date = (datetime.strptime(record.get("Posting Date"), "%m/%d/%Y") + timedelta(days=30) - timedelta(days=1)).strftime("%m/%d/%Y")

    account_type = record.get("Account Type")
    if account_type == "G_L_Account":
        account_type = "G/L Account"

    transformed_record = {
        "Journal_Template_Name": record.get("Journal Template Name"),
        "Journal_Batch_Name": "P-ACTUAL",
        "Account_No": record.get("Account No"),
        "Account_Type": account_type,
        "Document_No": fileMonth + "PAYROLL",
        "Amount": getAmount(record),
        "Shortcut_Dimension_1_Code": "" if record.get("Account No") in specialAccounts else record.get("DepartmentCode"),
        "Shortcut_Dimension_2_Code": "" if record.get("Account No") in specialAccounts else record.get("Cost Tracking"),
        "Mule_Posting_Date": mule_posting_date
        } 
    

    return transformed_record
