from typing import Optional
import pandas as pd
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="vandyshev-protected-workstation-audit-service",
    description="Учебный FastAPI-сервис для аудита рабочих станций (Vandyshev-21-K-AS1)",
    version="1.0.0",
)

workstations_data = [
    {"hostname": "ws-fin-01", "department": "Finance", "hardening_score": 92, "antivirus_enabled": True, "disk_encryption": True},
    {"hostname": "ws-hr-02", "department": "HR", "hardening_score": 88, "antivirus_enabled": True, "disk_encryption": True},
    {"hostname": "ws-dev-03", "department": "Engineering", "hardening_score": 79, "antivirus_enabled": True, "disk_encryption": False},
    {"hostname": "ws-soc-04", "department": "Security Operations", "hardening_score": 95, "antivirus_enabled": True, "disk_encryption": True},
    {"hostname": "ws-ops-05", "department": "Operations", "hardening_score": 83, "antivirus_enabled": False, "disk_encryption": True},
    {"hostname": "ws-legal-06", "department": "Legal", "hardening_score": 87, "antivirus_enabled": True, "disk_encryption": True},
]

workstations_df = pd.DataFrame(workstations_data)

def dataframe_to_records(dataframe: pd.DataFrame):
    return dataframe.to_dict(orient="records")

@app.get("/")
def read_root():
    return {
        "service": "vandyshev-protected-workstation-audit-service",
        "message": "Сервис аудита рабочих станций (Vandyshev-21-K-AS1)",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/workstations")
def get_workstations(department: Optional[str] = Query(default=None)):
    if department is None:
        filtered = workstations_df
    else:
        filtered = workstations_df[workstations_df["department"].str.casefold() == department.casefold()]
    return {"count": len(filtered), "workstations": dataframe_to_records(filtered)}

@app.get("/workstation/{hostname}")
def get_workstation(hostname: str):
    workstation = workstations_df[workstations_df["hostname"].str.casefold() == hostname.casefold()]
    if workstation.empty:
        raise HTTPException(status_code=404, detail="Workstation not found")
    return dataframe_to_records(workstation)[0]

@app.get("/audit-ready")
def get_audit_ready_workstations():
    ready = workstations_df[
        (workstations_df["hardening_score"] >= 85) &
        workstations_df["antivirus_enabled"] &
        workstations_df["disk_encryption"]
    ]
    dept_stats = ready["department"].value_counts().sort_index().to_dict()
    return {
        "message": "Рабочая станция готова к вводу в защищенный контур",
        "total_ready_workstations": len(ready),
        "department_distribution": dept_stats,
        "ready_workstations": dataframe_to_records(ready)
    }