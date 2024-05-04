from fastapi import APIRouter

# from .auth.controller import router as auth_router
from .fact_provider_service.controller import router as auth_router_fact
from .equi_hcpcs_phys.controller import router as auth_router_equi
from .drug_hcpcs_mftr.controller import router as auth_router_drug
from .aetna_billing_npi_geo.controller import router as auth_router_aetna
from .agg_cost.controller import router as auth_router_agg


router = APIRouter()
router.include_router(auth_router_fact)
router.include_router(auth_router_equi)
router.include_router(auth_router_drug)
router.include_router(auth_router_aetna)
router.include_router(auth_router_agg)