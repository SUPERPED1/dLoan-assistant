from app.core import *

# //////////////////// Calculate //////////////////
def calculate_dpi(income, debt, monthly = 0):
    dpi = int(((debt + monthly)/income) * 100)
    return dpi

def calculate_pmt(principal, interest, duration):
    r = (interest/100) / 12
    
    pmt = int((principal * r)*((1 + r)**duration) / (((1 + r)**duration) - 1))
    return pmt

def calculate_age(age, duration):
    f_age = int(age + (duration/12))
    return f_age

def age_score(age):
    if age <= 25:
        score = 1
    elif age <= 35:
        score = 2
    elif age <= 50:
        score = 3
    elif age <= 60:
        score = 2
    else:
        score = 0
        
    return score

def job_score(job):
    if job == "employee":
        score = 1
    else:
        score = 0
        
    return score

def salary_score(salary):
    if salary <= 35000:
        score = 1
    elif salary <= 50000:
        score = 2
    else:
        score = 3
        
    return score

def dti_score(dti):
    if dti <= 20:
        score = 3
    elif dti <= 40:
        score = 2
    elif dti <= 50:
        score = 1
    elif dti <= 60:
        score = -1
    else:
        score = 0
        
    return score

def future_dti_score(future_dti):
    if future_dti <= 20:
        score = 4
    elif future_dti <= 30:
        score = 3
    elif future_dti <= 40:
        score = 2
    elif future_dti <= 50:
        score = +1
    elif future_dti <= 60:
        score = -1
    elif future_dti <= 70:
        score = -2
    elif future_dti > 70:
        score = -3
        
    return score

def credit_history_score(history):
    if history == "normal":
        score = 4
    elif history == "none":
        score = 2
    else:
        score = 0
    
    return score

def collateral_score(collateral):
    if collateral != "" or collateral != "none":
        score = 2
    else:
        score = 0
    
    return score

def definition(total_score):
    if total_score >= 16:
        text = "ความเสี่ยงต่ำ"
    elif total_score >= 11:
        text = "ความเสี่ยงปานกลาง"
    elif total_score >= 6:
        text = "ความเสี่ยงสูง"
    else:
        text = "ความเสี่ยงสูงมาก"
    
    return text
    
# //////////////// Process ///////////////////
async def check_missing_data(payload):
    required_fields = [
        "applicant_id",
        "name",
        "age",
        "employment_type",
        "monthly_income",
        "monthly_debt",
        "requested_loan_amount",
        "credit_history",
        "duration",
    ]
    required_docs_employee = ["id_card", "salary_slip", "bank_statement"]
    required_docs_freelance, at_least_docs_freelance = ["id_card", "bank_statement"], {"withholding_tax_certificate", "tax_filing_report", "employment_contract"}
    required_docs_business, at_least_docs_business = ["id_card", "bank_statement", "commercial_registration_certificate"], {"p_p_30", "business_premises_photographs"}
    
    missing_field = [
        key for key in required_fields
        if (
            payload.get(key) is None
            or (isinstance(payload.get(key), str) and payload.get(key).strip() == "")
            or (isinstance(payload.get(key), (int, float)) and payload.get(key) < 0)
            or (isinstance(payload.get(key), list) and len(payload.get(key)) == 0)
        )
    ]
    
    if payload.get("employment_type"):
        employment_type = payload.get("employment_type")
        if employment_type == "employee":
            missing_doc = [doc for doc in required_docs_employee if doc not in payload["documents"]]
        elif employment_type == "freelance":
            missing_doc = [doc for doc in required_docs_freelance if doc not in payload["documents"]]
            if not (set(payload["documents"]) & at_least_docs_freelance):
                missing_doc.append(list(at_least_docs_freelance))
                
        elif employment_type == "business_owner":
            missing_doc = [doc for doc in required_docs_business if doc not in payload["documents"]]
            if not (set(payload["documents"]) & at_least_docs_business):
                missing_doc.append(list(at_least_docs_business))
        else:
            missing_doc = []
    else:
        missing_doc = []
    
    return missing_field, missing_doc

async def check_eligible_rule(payload, cal_data):
    Not_pass = []
    
    if payload["age"] < MINIMUM_AGE:
        Not_pass.append("ผู้ยื่นคำร้องมีอายุไม่ถึงเกณฑ์ 21 ปี")
    elif payload["age"] > MAXIMUM_AGE:
        Not_pass.append("ผู้ยื่นคำร้องมีอายุมากกว่าเกณฑ์ 60 ปี")
        
    if payload["employment_type"] not in ACCEPTED_EMPLOYMENT_TYPE:
        Not_pass.append("ผู้ยื่นคำร้องมีอาชีพที่ไม่อยู่ในเกณฑ์การคัดกรอง")
        
    if payload["monthly_income"] < MINIMUM_INCOME:
        Not_pass.append(f"ผู้ยื่นคำร้องมีเงินเดือนไม่ถึงเกณฑ์กำหนดขั้นต่ำ {MINIMUM_INCOME:,d} บาท")
        
    if payload["monthly_income"] != 0:
        future_net_income = payload["monthly_income"] - (payload["monthly_debt"] + cal_data["monthly_payment"])
        if cal_data["debt_to_income_ratio"] > MINIMUM_DTI:
            Not_pass.append(f"ผู้ยื่นคำร้องมีสัดส่วนหนี้สินต่อรายได้สูงกว่าเกณฑ์ {MINIMUM_DTI}%")
        elif future_net_income < MINIMUM_INCOME and cal_data["future_debt_to_income_ratio"] > MINIMUM_FUTURE_DTI:
            Not_pass.append(f"ผู้ยื่นคำร้องมีสัดส่วนหนี้สินต่อรายได้หากมีการผ่อนสินเชื่อสูงเกินกว่าเกณฑ์ 70% และมีหลายได้คงเหลือหลังหักค่าใช้จ่ายต่ำกว่า {MINIMUM_INCOME:,d} บาท")
            
    if payload["credit_history"] == "default":
        Not_pass.append("ผู้ยื่นคำร้องเคยมีประวัติค้างชำระ")
        
    return Not_pass

def calculate_risk_score(payload, cal_data):
    from app.schemas import RiskScore

    # คำนวนคะแนนอายุ
    age = age_score(payload["age"])
    job = job_score(payload["employment_type"])
    salary = salary_score(payload["monthly_income"])
    dti = dti_score(cal_data["debt_to_income_ratio"])
    credit_history = credit_history_score(payload["credit_history"])
    collateral = collateral_score(payload["collateral"])
    future_dti = future_dti_score(cal_data["future_debt_to_income_ratio"])
    
    total_score = age + job + salary + dti + credit_history + collateral + future_dti
    
    text = definition(total_score)
    
    return RiskScore(
        total_score= total_score,
        definition=text
    )
    

async def prepare_data(payload):
    format = {
        "debt_to_income_ratio" : 0,
        "monthly_payment" : 0,
        "future_debt_to_income_ratio": 0,
        "age_finish": 0
    }
    
    format["debt_to_income_ratio"] = calculate_dpi(payload["monthly_income"], payload["monthly_debt"])
    
    format["monthly_payment"] = calculate_pmt(payload["requested_loan_amount"], STATIC_INTEREST, payload["duration"])
    
    format["future_debt_to_income_ratio"] = calculate_dpi(payload["monthly_income"], payload["monthly_debt"], format["monthly_payment"])
    
    format["age_finish"] = calculate_age(payload["age"], payload["duration"])
    
    return format
    