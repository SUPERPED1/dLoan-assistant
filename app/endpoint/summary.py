from fastapi import APIRouter, status
from app.schemas import InputFormat, APIResponse
from app.services import data, model
from app.core import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/summary")


@router.post("", response_model=APIResponse, response_model_exclude_none=True)
async def analytic(payload:InputFormat):
    payload = payload.model_dump()
    
    # ตรวจสอบข้อมูลและเอกสารว่าสูญหายหรือไม่
    is_field_missing, is_docs_missing = await data.check_missing_data(payload)
    if is_field_missing or is_docs_missing:
        logger.info(f"Applicant id [{payload["applicant_id"]}] - Missing document or information on [{is_field_missing}, {is_docs_missing}]")
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
        logger.info(f"Applicant id [{payload["applicant_id"]}] - Not pass the regulator rule in [{reason}]")
        return APIResponse(
            applicant_data = payload,
            status = "Reject/ Not Eligible",
            reason = reason,
            financials=cal_data
        )
    
    # Test
    risk_score = data.calculate_risk_score(payload, cal_data)
    
    # เตรียมข้อมูลให้กับโมเดล
    prompt = model.user_prompt_generate(payload, cal_data)
    # Prompt agent role and create test case
    result = await model.typhoon_agent(prompt)
    
    logger.info(
        "Applicant id [%s] - Analysis completed | Status=%s | RiskScore=%s | RiskFlags=%s",
        payload["applicant_id"],
        result["recommendation"],
        risk_score,
        result["risk_flags"]
    )
    return APIResponse(
        applicant_data=payload,
        status= result["recommendation"],
        financials=cal_data,
        risk=result["risk_flags"],
        explanation=result["explanation"],
        risk_score = risk_score
    )