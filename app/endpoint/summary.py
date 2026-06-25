from fastapi import APIRouter, status
from app.schemas import InputFormat, APIResponse
from app.services import data, model


router = APIRouter(prefix="/summary")


@router.post("", response_model=APIResponse, response_model_exclude_none=True)
async def analytic(payload:InputFormat):
    payload = payload.model_dump()
    
    # ตรวจสอบข้อมูลและเอกสารว่าสูญหายหรือไม่
    is_field_missing, is_docs_missing = await data.check_missing_data(payload)
    if is_field_missing or is_docs_missing:
        return APIResponse(
            applicant_data = payload,
            status = "Need more information",
            missing_fields = is_field_missing,
            missing_documents = is_docs_missing
        )

    cal_data = await data.prepare_data(payload)
    
    # ตรวจสอบใบขอสินเชื่อว่าผ่านเกณฑ์ที่กำหนดเบื้องต้นหรือไม่
    reason = await data.check_eligible_rule(payload, cal_data)
    if reason:
        return APIResponse(
            applicant_data = payload,
            status = "Reject/ Not Eligible",
            reason = reason,
            financials=cal_data
        )
    
    # เตรียมข้อมูลให้กับโมเดล
    
    prompt = model.user_prompt_generate(payload, cal_data)
    # Prompt agent role and create test case
    result = await model.typhoon_agent(prompt)
    
    return APIResponse(
        applicant_data=payload,
        status= result["recommendation"],
        financials=cal_data,
        risk=result["risk_flags"],
        explanation=result["explanation"]
    )