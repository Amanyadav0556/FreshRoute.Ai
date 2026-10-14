"""Scientific, economic and logistical assumptions disclosure endpoints."""
from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

ASSUMPTIONS_REGISTRY: List[Dict[str, Any]] = [
    {
        "id": "asm-01",
        "category": "Demand Elasticity",
        "parameter": "Price Elasticity of Demand (ε)",
        "value": "-1.35 for Tomatoes, -1.80 for Spinach",
        "provenance": "estimated",
        "provenance_source": "ICAR-NIAP Agricultural Price Elasticity Study",
        "notes": "Higher elasticity for perishable greens indicates buyers rapidly respond to clearance discounting.",
    },
    {
        "id": "asm-02",
        "category": "Shelf-Life Degradation",
        "parameter": "Q10 Respiration Acceleration Factor",
        "value": "2.2 to 2.8 per 10°C increase",
        "provenance": "real",
        "provenance_source": "USDA Agriculture Handbook 66 & FAO Post-Harvest Manual",
        "notes": "Biological produce decay doubles for every 10°C ambient rise above 20°C.",
    },
    {
        "id": "asm-03",
        "category": "Cold-Chain Impact",
        "parameter": "Refrigerated Transport Decay Multiplier",
        "value": "0.35x baseline ambient rate",
        "provenance": "estimated",
        "provenance_source": "NCCD India Cold-Chain Logistics Benchmark",
        "notes": "Maintains temperature at 4-6°C, decelerating microbial spoilage by ~65%.",
    },
    {
        "id": "asm-04",
        "category": "Logistics & Transport",
        "parameter": "Vehicle Operating Freight Cost",
        "value": "₹11.50 - ₹14.00/km (Mini-trucks), ₹22.00/km (Reefer)",
        "provenance": "real",
        "provenance_source": "Nashik Goods Transport Association (NGTA) Tariff Card",
        "notes": "Reflects prevailing commercial diesel prices and driver allowances in Maharashtra.",
    },
    {
        "id": "asm-05",
        "category": "Logistics & Transport",
        "parameter": "Ghat Road Transit Vibration Factor",
        "value": "1.10 - 1.30x stress multiplier",
        "provenance": "estimated",
        "provenance_source": "CIRCOT / ICAR Post-Harvest Engineering Reports",
        "notes": "Vibration on ghat roads (Kasara/Malshej) accelerates tomato skin bruising.",
    },
    {
        "id": "asm-06",
        "category": "Mandi Operations",
        "parameter": "APMC Mandi Unloading & Handling Fee",
        "value": "₹0.45 - ₹0.85 per kg",
        "provenance": "real",
        "provenance_source": "Maharashtra Agricultural Marketing Board (MSAMB)",
        "notes": "Mathadi labour and mandi cess statutory deductions.",
    },
    {
        "id": "asm-07",
        "category": "Economic Salvage",
        "parameter": "Agro-Processor Offtake Contract Floor",
        "value": "95% of farmer procurement cost",
        "provenance": "estimated",
        "provenance_source": "Commercial food processing puree/paste contracts",
        "notes": "Guarantees bulk clearance for Grade B/C tomatoes and mangoes.",
    },
    {
        "id": "asm-08",
        "category": "Economic Salvage",
        "parameter": "Institutional Food Bank Tax Deduction",
        "value": "40% equivalent procurement cost value",
        "provenance": "real",
        "provenance_source": "Section 80G Indian Income Tax Act",
        "notes": "Allows corporate charitable write-off for produce redirected to feeding charities.",
    },
]


@router.get("", response_model=List[Dict[str, Any]])
async def list_assumptions():
    """Discloses all 8 core scientific, economic, and logistical assumptions with provenance."""
    return [
        {
            **item,
            "source": item.get("provenance", "real"),
            "note": item.get("notes", ""),
        }
        for item in ASSUMPTIONS_REGISTRY
    ]
