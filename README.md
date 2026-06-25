# 🏦 Loan Approval System

ระบบประเมินสินเชื่อด้วย Generative AI

---

## 📁 โครงสร้างไฟล์

```
loan-approval/
├── backend/
│   ├── main.py           ← FastAPI backend (จุดแก้ไขมาร์คไว้ทั้งหมด)
│   └── requirements.txt
└── frontend/
    └── index.html        ← UI ทั้งหมดในไฟล์เดียว
```

---

## 🚀 วิธีติดตั้งและรัน

### 1. Backend (FastAPI)

```bash
cd backend

# ติดตั้ง dependencies
pip install -r requirements.txt

# ตั้งค่า API Key
export ANTHROPIC_API_KEY="sk-ant-..."

# รัน server
python main.py
# หรือ
uvicorn main:app --reload --port 8000
```

API จะรันที่ `http://localhost:8000`
Swagger docs: `http://localhost:8000/docs`

### 2. Frontend

เปิดไฟล์ `frontend/index.html` ด้วย browser โดยตรง
หรือใช้ VS Code Live Server (port 5500)

---

## 🔧 จุดที่แก้ไขได้ (Edit Points)

ไฟล์ทั้งสองมีการมาร์คจุดแก้ไขในรูปแบบ:
```
# [EDIT: ชื่อจุด] — คำอธิบาย
...โค้ดที่แก้ไขได้...
# [/EDIT]
```

### main.py — จุดสำคัญ

| จุด | คำอธิบาย |
|-----|---------|
| `ELIGIBILITY_RULES` | กฎเกณฑ์คุณสมบัติ (อายุ, รายได้, DTI) |
| `HIGH_RISK_THRESHOLDS` | เกณฑ์ความเสี่ยงสูง |
| `INTEREST_RATE` | อัตราดอกเบี้ย |
| `CREDIT_HISTORY_SCORE` | คะแนนตามประวัติเครดิต |
| `DTI_SCORE` | คะแนนตาม DTI |
| `SYSTEM_PROMPT` | บทบาทของ AI |
| `USER_PROMPT` | รูปแบบข้อมูลที่ส่ง AI |
| `FINAL_RECOMMENDATION_LOGIC` | ตรรกะสรุปผล |
| `SAVE_TO_DB` | บันทึก Audit Log |
| `ANTHROPIC_CONFIG` | API Key และ Model |
| `CORS_ORIGINS` | Domain ที่อนุญาต |

### index.html — จุดสำคัญ

| จุด | คำอธิบาย |
|-----|---------|
| `CSS_VARIABLES` | สีและ theme |
| `API_BASE_URL` | URL ของ Backend |
| `EMPLOYMENT_OPTIONS` | ตัวเลือกอาชีพ |
| `DOCUMENT_TYPES` | ประเภทเอกสาร |
| `STATUS_MAP` | แมป recommendation → สี/ไอคอน |
| `RISK_SCORE_COLORS` | สี Risk Score Bar |
| `DTI_COLOR_THRESHOLDS` | สีของ DTI preview |
| `TOAST_DURATION` | ระยะเวลาแสดง notification |

---

## 🔄 API Endpoints

| Method | Path | คำอธิบาย |
|--------|------|---------|
| POST | `/evaluate` | ประเมินคำขอสินเชื่อ |
| POST | `/audit/log` | บันทึกการตัดสินใจ |
| GET  | `/health` | ตรวจสอบสถานะ |
| GET  | `/docs` | Swagger UI |

---

## 📊 ผลลัพธ์การประเมิน 4 ประเภท

| สถานะ | ความหมาย | สี |
|-------|---------|-----|
| ✅ Proceed | ผ่านเกณฑ์ | เขียว |
| 📋 Need More Info | ข้อมูล/เอกสารไม่ครบ | เหลือง |
| 🚫 Reject / Not Eligible | ไม่ผ่านเกณฑ์ | แดง |
| ⚠️ High Risk Review | ผ่านแต่เสี่ยงสูง | ส้ม |
