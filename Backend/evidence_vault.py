# ==========================================
# SAFESPHERE EVIDENCE VAULT
# ==========================================

from supabase_client import supabase


def save_case(
    case_name,
    summary,
    indicators,
    assessment,
    timeline,
    safety_plan
):
    """Save a SafeSphere analysis to Supabase."""

    try:
        data = {
            "case_name": case_name,
            "summary": summary,
            "concern_level": assessment.get("level"),
            "risk_score": assessment.get("score"),
            "indicators": indicators,
            "timeline": timeline,
            "safety_plan": safety_plan
        }

        response = (
            supabase
            .table("evidence_vault")
            .insert(data)
            .execute()
        )

        return {
            "success": True,
            "data": response.data
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


def get_cases():
    """Get all saved SafeSphere cases."""

    try:
        response = (
            supabase
            .table("evidence_vault")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return {
            "success": True,
            "data": response.data
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


def get_case(case_id):
    """Get one case by ID."""

    try:
        response = (
            supabase
            .table("evidence_vault")
            .select("*")
            .eq("id", case_id)
            .execute()
        )

        if not response.data:
            return {
                "success": False,
                "error": "Case not found"
            }

        return {
            "success": True,
            "data": response.data[0]
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }