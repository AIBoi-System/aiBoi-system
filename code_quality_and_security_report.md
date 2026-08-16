# Code Quality and Security Report

This report presents the findings of the static analysis and manual security review conducted on the Python backend codebase for **AiBoi-system** (under `backend/app`).

---

## 1. Executive Summary

| Area | Status | Key Findings |
| :--- | :--- | :--- |
| **Static Security (Bandit)** | 🟢 Pass | 0 vulnerabilities detected by static analysis tools. |
| **Cyclomatic Complexity (Radon)** | 🟢 Excellent | Average complexity is **A (1.83)**. Extremely modular. |
| **Maintainability Index (Radon)** | 🟢 Excellent | **100% of files scored A**. Low technical debt. |
| **Manual Security & Architecture Review** | 🔴 Critical | **Severe BOLA** (Broken Object Level Authorization) and **Missing Authentication** on administrative/user routes. |

---

## 2. Static Analysis Metrics

### A. Bandit Security Scan
* **Command run**: `bandit -r backend/app`
* **Lines of code scanned**: 4,885
* **Vulnerabilities found**: 0
* **Result**: Static analysis indicates good base practices (no raw usage of `eval`, insecure temporary files, or basic shell injection vectors).

### B. Radon Cyclomatic Complexity (CC)
* **Command run**: `radon cc backend/app -a`
* **Average Complexity**: **A (1.835)** (Very low complexity)
* **Blocks with complexity > A**:
  * **C (Moderate Complexity)**:
    * `ReproductionService._ensure_step_sequence` ([reproduction_service.py](file:///c:/Users/sandr/aiBoi-system/backend/app/modules/inventory/application/reproduction_service.py)) — *Complexity: 11* (Handles reproductive steps progression).
  * **B (Low-Medium Complexity)**:
    * `ReproductionService.create_step_execution` ([reproduction_service.py](file:///c:/Users/sandr/aiBoi-system/backend/app/modules/inventory/application/reproduction_service.py))
    * `UpdateAnimalUseCase.execute` ([use_cases.py](file:///c:/Users/sandr/aiBoi-system/backend/app/modules/inventory/application/use_cases.py))
    * `PropertyService.update_property` ([property_service.py](file:///c:/Users/sandr/aiBoi-system/backend/app/shared/application/property/property_service.py))
    * `update_owner_service` ([owner_service.py](file:///c:/Users/sandr/aiBoi-system/backend/app/shared/application/user/owner_service.py))
    * `CPF.validar` ([cpf.py](file:///c:/Users/sandr/aiBoi-system/backend/app/shared/infrastructure/persistence/cpf.py))
    * `update_owner` ([owner_repository.py](file:///c:/Users/sandr/aiBoi-system/backend/app/shared/infrastructure/persistence/owner_repository.py))
    * `validate_password_strength` ([security_validators.py](file:///c:/Users/sandr/aiBoi-system/backend/app/core/security_validators.py))
    * `_parse_br_date` ([date_types.py](file:///c:/Users/sandr/aiBoi-system/backend/app/presentation/schemas/common/date_types.py))
    * `SmtpEmailService._send` ([smtp_service.py](file:///c:/Users/sandr/aiBoi-system/backend/app/infrastructure/email/smtp_service.py))

### C. Radon Maintainability Index (MI)
* **Command run**: `radon mi backend/app`
* **Result**: **100% of files scored A** (Maintainability Index >= 80). The codebase is highly readable and structure is clean.

---

## 3. Manual Security Review Findings (Against API Security Guidelines)

### Finding 1: Missing Authentication & Authorization (Critical Risk)
* **Affected Files**:
  * [address_router.py](file:///c:/Users/sandr/aiBoi-system/backend/app/presentation/api/v1/address_router.py)
  * [owner_router.py](file:///c:/Users/sandr/aiBoi-system/backend/app/presentation/api/v1/owner_router.py)
  * [user_router.py](file:///c:/Users/sandr/aiBoi-system/backend/app/presentation/api/v1/user_router.py)
* **Description**: These routers do not declare dependency on `current_user=Depends(get_current_user)`.
* **Impact**: Unauthenticated users can perform CRUD operations on all users, owners, addresses, and upgrade arbitrary users to system owners.

### Finding 2: Broken Object-Level Authorization (BOLA) in Owner Modules (High Risk)
* **Affected File**: [owner_module_router.py](file:///c:/Users/sandr/aiBoi-system/backend/app/presentation/api/v1/owner_module_router.py#L27-L33)
* **Description**: The endpoint `GET /owner-modules/{owner_id}` enforces `require_roles("owner", "admin")`, but does not verify that the authenticated owner's `id_user` matches the requested `owner_id`.
* **Impact**: Any authenticated owner can inspect the modules (features) assigned to other owners.

### Finding 3: Default Insecure JWT Configuration & Lack of Fail-Fast Secret Key (Medium Risk)
* **Affected File**: [auth.py](file:///c:/Users/sandr/aiBoi-system/backend/app/shared/infrastructure/auth/auth.py#L10)
* **Description**: The application falls back to `"your-secret-key"` if `JWT_SECRET_KEY` is missing in the environment. It does not enforce a strong key nor fail to boot if it's missing, violating the checklist: *"Aplicacao falha ao iniciar sem chave JWT forte."*
* **Impact**: Weak defaults increase signature forgery risks.

### Finding 4: Exposure of Sensitive Data (Full CPF in API Payload) (Medium Risk)
* **Affected Files**:
  * [user_response.py](file:///c:/Users/sandr/aiBoi-system/backend/app/presentation/schemas/user/user_response.py#L11)
  * [owner_response.py](file:///c:/Users/sandr/aiBoi-system/backend/app/presentation/schemas/owner/owner_response.py#L11)
* **Description**: The schemas return the full CPF number in plaintext. This violates the guideline: *"Nunca registrar ou retornar segredo, senha, token ou CPF completo."*
* **Impact**: Exposure of PII data, leading to GDPR/LGPD compliance issues.

### Finding 5: Blocklist-based Input Validation Anti-Pattern (Usability & Design Defect)
* **Affected File**: [security_validators.py](file:///c:/Users/sandr/aiBoi-system/backend/app/core/security_validators.py#L7-L23)
* **Description**: `validate_safe_text` filters out standard punctuation like `'` (single quote) and `"` (double quote) to prevent SQL injection in text input fields (name, street, complement).
* **Impact**: Valid user inputs like name `O'Connor` or addresses with quotes are rejected. The database uses SQLAlchemy ORM parameterized queries, rendering blocklist-based filtering redundant and harmful to usability.

### Finding 6: Permissive Default CORS Configuration (Low Risk)
* **Affected File**: [main.py](file:///c:/Users/sandr/aiBoi-system/backend/app/main.py#L18)
* **Description**: Defaults to `*` if the `CORS_ALLOWED_ORIGINS` environment variable is not defined, violating the requirement: *"CORS possui origens explicitas por ambiente."*

---

## 4. Remediation Plan

### Remediation 1: Secure open routers with Authentication
Apply authentication dependencies to all routes in `address_router.py`, `owner_router.py`, and `user_router.py`.

```python
# Example for user_router.py
from app.presentation.api.auth_dependencies import get_current_user

@router.get("/", response_model=list[UserResponseSchema])
def list_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user) # Require auth
):
    ...
```

### Remediation 2: Implement BOLA check in Owner Modules router
Verify that the current user is an admin, or that their ID matches the target resource:

```python
@router.get(
    "/{owner_id}",
    response_model=List[OwnerModuleResponse],
)
def list_modules(
    owner_id: int, 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.type != "admin" and current_user.id_user != owner_id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
    return OwnerModuleService.list_owner_modules(db, owner_id)
```

### Remediation 3: Mask CPF in API responses
Modify the Pydantic schemas to mask the CPF or exclude it from the serialization payload unless explicitly required by an authorized role.

```python
# Masking example in Pydantic:
from pydantic import field_validator

class UserResponseSchema(BaseModel):
    # ...
    cpf: str

    @field_validator("cpf")
    @classmethod
    def mask_cpf(cls, v: str) -> str:
        # e.g., returns "123.***.***-45"
        if len(v) == 14: # Assuming formatted "123.456.789-01"
            return f"{v[:3]}.***.***-{v[-2:]}"
        return "***.***.***-**"
```

### Remediation 4: Enforce strong JWT secrets on Startup
Raise an error if `JWT_SECRET_KEY` is not present, or if it is shorter than 32 characters or equal to `"your-secret-key"`.

```python
# In auth.py
if not SECRET_KEY or SECRET_KEY == "your-secret-key" or len(SECRET_KEY) < 32:
    raise RuntimeError("A chave JWT_SECRET_KEY não está configurada ou é fraca.")
```

### Remediation 5: Remove quote blocklist from Safe Text Validator
Rely on SQLAlchemy parameterization for SQLi prevention. Adjust `_FORBIDDEN_SUBSTRINGS` to only block actual HTML/script injection tags (XSS) if needed, rather than single and double quotes.
