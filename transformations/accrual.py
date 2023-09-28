from datetime import datetime, timedelta
import re

def combined_transformation(payload_row):
    special_accounts = ["10300", "10310", "11220", "21040", "21100", "21150", "22320", "22340"]
    original_filename = "Accrual_GL_Payroll_04302023.csv"

    def get_next_first_date(date_str):
        date_obj = datetime.strptime(date_str, "%m%d%Y")
        next_first = date_obj.replace(day=1) + timedelta(days=31)
        next_first -= timedelta(days=next_first.day)
        return next_first.strftime("%m/%d/%Y")
    
    filtered_data = []
    grouped_special = {}
    grouped_rest = {}
    
    for rec in payload_row:
        if rec["Account No"] not in special_accounts:
            filtered_data.append(rec)
            group_key = f"{rec['Posting Date']}-{rec['Account No']}"
            grouped_special.setdefault(group_key, []).append(rec)
        else:
            group_key = f"{rec['Posting Date']}-{rec['Account No']}-{rec['DepartmentCode']}-{rec['Cost Tracking']}"
            grouped_rest.setdefault(group_key, []).append(rec)
    
    transformed_data = []
    
    for group in grouped_special.values():
        total_debit = sum(float(rec["Debit Amount"]) for rec in group)
        total_credit = sum(float(rec["Credit Amount"]) for rec in group)
        
        transformed_rec = {
            "Journal Template Name": group[0]["Journal Template Name"],
            "Journal Batch Name": group[0]["Journal Batch Name"],
            "Posting Date": group[0]["Posting Date"],
            "Account Type": group[0]["Account Type"],
            "Account No": group[0]["Account No"],
            "Document No": group[0]["Document No"],
            "Debit Amount": total_debit,
            "Credit Amount": total_credit,
            "DepartmentCode": "",
            "Cost Tracking": ""
        }
        
        transformed_data.append(transformed_rec)
    
    for group in grouped_rest.values():
        total_debit = sum(float(rec["Debit Amount"]) for rec in group)
        total_credit = sum(float(rec["Credit Amount"]) for rec in group)
        
        transformed_rec = {
            "Journal Template Name": group[0]["Journal Template Name"],
            "Journal Batch Name": group[0]["Journal Batch Name"],
            "Posting Date": group[0]["Posting Date"],
            "Account Type": group[0]["Account Type"],
            "Account No": group[0]["Account No"],
            "Document No": group[0]["Document No"],
            "Debit Amount": total_debit,
            "Credit Amount": total_credit,
            "DepartmentCode": group[0]["DepartmentCode"],
            "Cost Tracking": group[0]["Cost Tracking"]
        }
        
        transformed_data.append(transformed_rec)
    
    transformed_data.sort(key=lambda x: datetime.strptime(x["Posting Date"], "%m/%d/%Y"))
    
    result = []
    
    for rec in transformed_data:
        credit_amount = float(rec["Credit Amount"])
        debit_amount = float(rec["Debit Amount"])
        
        if credit_amount + debit_amount != 0:
            file_date = re.search(r'_(\d{8})\.csv', original_filename).group(1)
            file_date_obj = datetime.strptime(file_date, "%m%d%Y")
            file_month = file_date_obj.strftime("%b").upper()
            
            posting_date = datetime.strptime(rec["Posting Date"], "%m/%d/%Y")
            posting_date_str = posting_date.strftime("%m/%d/%Y")
            
            next_first_date = get_next_first_date(file_date)
            
            if posting_date_str == next_first_date:
                mule_posting_date = posting_date_str
            else:
                next_first_date_obj = datetime.strptime(next_first_date, "%m/%d/%Y")
                mule_posting_date = (next_first_date_obj - timedelta(days=1)).strftime("%m/%d/%Y")
            
            transformed_rec = {
                "Journal_Template_Name": rec["Journal Template Name"],
                "Journal_Batch_Name": "P-ACCRUAL",
                "Account_No": rec["Account No"],
                "Account_Type": rec["Account Type"].upper(),
                "Document_No": f"{file_month} PR ACCRUAL",
                "Amount": -credit_amount + debit_amount,
                "Shortcut_Dimension_1_Code": rec["DepartmentCode"],
                "Shortcut_Dimension_2_Code": rec["Cost Tracking"],
                "Mule_Posting_Date": mule_posting_date
            }
            
            result.append(transformed_rec)
    
    result.sort(key=lambda x: datetime.strptime(x["Mule_Posting_Date"], "%m/%d/%Y"))
    return result
