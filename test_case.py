test_cases = [
    # Eligible case: 3 Case
    # Purpose: เพื่อทดสอบโมเดลสามารถสรุปผลและสร้างคำแนะนำ การตัดสินใจจากข้อมูลใบสมัครสินเชื่อได้หรือไม่
    # ผลลัพท์ที่คาดหวัง: โมเดลตอบกลับมาเป็น Passed ในทุกคำตอบ และมีการอธิบายเหตุผลรวมถึงคำแนะนำกลับมา
    # 1. Normal case employee
    {
        "applicant_id": "APP001",
        "name": "Somchai",
        "age": 32,
        "employment_type": "employee",
        "monthly_income": 35000,
        "monthly_debt": 12000,
        "requested_loan_amount": 200000,
        "credit_history": "normal",
        "duration": 36,
        "collateral": "car",
        "documents": ["id_card", "salary_slip", "bank_statement"],
        "notes": "Stable job for 3 years"
    },

    # 2. Normal case freelance
    {
        "applicant_id": "APP002",
        "name": "Anan",
        "age": 28,
        "employment_type": "freelance",
        "monthly_income": 50000,
        "monthly_debt": 15000,
        "requested_loan_amount": 300000,
        "credit_history": "normal",
        "duration": 48,
        "collateral": "house",
        "documents": ["id_card", "bank_statement", "tax_filing_report", "employment_contract"],
        "notes": "Income around 45000 to 60000 per month"
    },

    # 3. Normal case business owner
    {
        "applicant_id": "APP003",
        "name": "Porn",
        "age": 40,
        "employment_type": "business_owner",
        "monthly_income": 150000,
        "monthly_debt": 50000,
        "requested_loan_amount": 500000,
        "credit_history": "normal",
        "duration": 60,
        "collateral": "none",
        "documents": ["id_card", "bank_statement", "commercial_registration_certificate", "p_p_30", "business_premises_photographs"],
        "notes": "Own best company award"
    },
    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 	# Applicants with missing documents: 3 Case
    # Purpose: เพื่อทดสอบระบบในการตรวจสอบความครบถ้วนของข้อมูลและเอกสารหรือไม่
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Need information และ บอกถึงเอกสารหรือข้อมูลที่ขาดหายไปว่ามีอะไรบ้าง
    
    # 4. Missing documents (freelance)
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Need information โดยบอกข้อมูลสูญหายใน
    # "missing_fields" = []
    # "missing_documents" = "bank_statement" "withholding_tax_certificate" "tax_filing_report" "employment_contract"
    {
        "applicant_id": "APP004",
        "name": "Krit",
        "age": 25,
        "employment_type": "freelance",
        "monthly_income": 25000,
        "monthly_debt": 2000,
        "requested_loan_amount": 80000,
        "credit_history": "none",
        "duration": 24,
        "collateral": "none",
        "documents": ["id_card"],
        "notes": "First loan"
    },

    # 5. Missing documents (employee)
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Need information โดยบอกข้อมูลสูญหายใน
    # "missing_fields" = []
    # "missing_documents" = "bank_statement"
    {
        "applicant_id": "APP005",
        "name": "Nok",
        "age": 38,
        "employment_type": "employee",
        "monthly_income": 40000,
        "monthly_debt": 15000,
        "requested_loan_amount": 150000,
        "credit_history": "bad",
        "duration": 24,
        "collateral": "car",
        "documents": ["id_card", "salary_slip"],
        "notes": "Past default"
    },

    # 6. Missing multiple field data
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Need information โดยบอกข้อมูลสูญหายใน
    # "missing_fields" = ["employment_type", "credit_history"]
    # "missing_documents" = ["id_card", "salary_slip", "bank_statement"]
    {
        "applicant_id": "APP006",
        "name": "Preecha",
        "age": 45,
        "employment_type": "",
        "monthly_income": 0,
        "monthly_debt": 10000,
        "requested_loan_amount": 250000,
        "credit_history": "",
        "duration": 60,
        "collateral": "land",
        "documents": [],
        "notes": ""
    },

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 	# Low income applicants: 2 Case
    # Purpose: เพื่อทดสอบการตัดสินใจของโมเดลในกรณีที่มีเงินเดือนต่ำ
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Passed หรือ High risk review
    
    # 7. Low income normal debt
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Passed เนื่องจาก DTI ยังไม่เกินเกณฑ์ที่กำหนดไว้และความเหมาะสมของระยะเวลากับเงินผ่อนต่อเดือน
    {
        "applicant_id": "APP007",
        "name": "Som",
        "age": 30,
        "employment_type": "employee",
        "monthly_income": 21000,
        "monthly_debt": 5000,
        "requested_loan_amount": 50000,
        "credit_history": "normal",
        "duration": 36,
        "collateral": "none",
        "documents": ["id_card", "salary_slip", "bank_statement"],
        "notes": ""
    },

    # 8. Low income, high debt
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น High risk review โดยมีความเสี่ยงเกี่ยวกับ DTI ที่เพิ่มสูงขึ้นในอนาคต
    {
        "applicant_id": "APP008",
        "name": "Lek",
        "age": 28,
        "employment_type": "employee",
        "monthly_income": 21000,
        "monthly_debt": 10000,
        "requested_loan_amount": 80000,
        "credit_history": "none",
        "duration": 24,
        "collateral": "none",
        "documents": ["id_card", "salary_slip", "bank_statement"],
        "notes": ""
    },

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 	# High debt-to-income applicants: 2 Case
    # Purpose: เพื่อทดสอบระบบในการคัดกรอง หรือ ตอบกลับของโมเดลในกรณีที่มี DTI สูงกว่าปกติ
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น High risk review หรือ ไม่ผ่านเกณฑ์เนื่องจากมี DTI ที่สูงกว่าเกณฑ์ที่กำหนดไว้
    
    # 9. High dti almost 80%
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับ Reject โดยให้เหตุผลว่า มีสัดส่วนหนี้สินต่อรายได้ไม่ผ่านเกณฑ์
    {
        "applicant_id": "APP009",
        "name": "Chai",
        "age": 50,
        "employment_type": "employee",
        "monthly_income": 200000,
        "monthly_debt": 160000,
        "requested_loan_amount": 5000000,
        "credit_history": "normal",
        "duration": 120,
        "collateral": "building",
        "documents": ["id_card", "salary_slip", "bank_statement"],
        "notes": "House loan"
    },

    # 10. High dti ไม่มีของคำ้ประกัน
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Rejected และให้เหตุผล สัดส่วนหนี้สินต่อรายได้หากมีการผ่อนสินเชื่อสูงเกินกว่าเกณฑ์ 70% และมีหลายได้คงเหลือหลังหักค่าใช้จ่ายต่ำกว่า 20,000 บาท
    {
        "applicant_id": "APP010",
        "name": "Mint",
        "age": 21,
        "employment_type": "employee",
        "monthly_income": 20000,
        "monthly_debt": 10000,
        "requested_loan_amount": 200000,
        "credit_history": "none",
        "duration": 24,
        "collateral": "none",
        "documents": ["id_card", "salary_slip", "bank_statement"],
        "notes": ""
    },

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 	# Applicants with risky credit history: 2 Case
    # Purpose: เพื่อทดสอบการตัดสินใจของโมเดลในกรณีที่ credit history มีความเสี่ยงที่สูง
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น High risk review หรือ Rejected โดยให้เหตุผลเกี่ยวข้องกับความเสี่ยงด้านเครดิต 

    # 11. Credit history is late
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น High risk review โดยให้เหตุผลเกี่ยวข้องกับความเสี่ยงด้านเครดิตที่เคยทีประวัติการจ่ายเงินล่าช้า 
    {
        "applicant_id": "APP011",
        "name": "Suda",
        "age": 42,
        "employment_type": "employee",
        "monthly_income": 30000,
        "monthly_debt": 10000,
        "requested_loan_amount": 50000,
        "credit_history": "late",
        "duration": 24,
        "collateral": "none",
        "documents": ["id_card", "salary_slip", "bank_statement"],
        "notes": ""
    },

    # 12. Credit history is default
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Rejected โดยให้เหตุผลเนื่องจากผู้ยื่นคำร้องเคยมีประวัติค้างชำระหนี้ 
    {
        "applicant_id": "APP012",
        "name": "Moon",
        "age": 35,
        "employment_type": "employee",
        "monthly_income": 30000,
        "monthly_debt": 2000,
        "requested_loan_amount": 100000,
        "credit_history": "default",
        "duration": 36,
        "collateral": "car",
        "documents": ["id_card", "salary_slip", "bank_statement"],
        "notes": ""
    },

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 	# Invalid Case: 3 Case
    # Purpose: เพื่อทดสอบการคัดกรองจากกฎพื้นฐานที่ตั้งไว้ของระบบ
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Rejected พร้อมให้เหตุผลในการปัดตก
    
    # 13. Too young and employment_type is student
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Rejected พร้อมให้เหตุผล 1) อายุไม่ถึงเกณฑ์ 2. อาชีพไม่รองรับ
    {
        "applicant_id": "APP013",
        "name": "Man",
        "age": 18,
        "employment_type": "student",
        "monthly_income": 30000,
        "monthly_debt": 8000,
        "requested_loan_amount": 30000,
        "credit_history": "none",
        "duration": 12,
        "collateral": "",
        "documents": ["id_card", "bank_statement"],
        "notes": ""
    },

    # 14. Income less than minimum
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Rejected พร้อมให้เหตุผล 1. รายได้ไม่ผ่านเกณฑ์ชั้นต่ำ 20000 บาท
    {
        "applicant_id": "APP014",
        "name": "BigDoc",
        "age": 42,
        "employment_type": "employee",
        "monthly_income": 18000,
        "monthly_debt": 2000,
        "requested_loan_amount": 50000,
        "credit_history": "normal",
        "duration": 12,
        "collateral": "car",
        "documents": ["id_card", "salary_slip", "bank_statement"],
        "notes": ""
    },

    # 15. อาชีพไม่อยู่ในเกณฑ์
    # ผลลัพท์ที่คาดหวัง: ระบบตอบกลับเป็น Rejected พร้อมให้เหตุผล 1. อาชีพไม่รองรับ
    {
        "applicant_id": "APP015",
        "name": "Blue",
        "age": 30,
        "employment_type": "farmer",
        "monthly_income": 25000,
        "monthly_debt": 5000,
        "requested_loan_amount": 70000,
        "credit_history": "none",
        "duration": 18,
        "collateral": "none",
        "documents": ["id_card"],
        "notes": ""
    }
]