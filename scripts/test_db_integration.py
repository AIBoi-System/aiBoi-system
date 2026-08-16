import sys
import secrets
import random
from pathlib import Path
import traceback
from dotenv import load_dotenv

# Set up paths
ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

# Ensure root .env is loaded
load_dotenv(dotenv_path=ROOT_DIR / ".env")

# Now import FastAPI App and other dependencies
from fastapi.testclient import TestClient
from app.main import app
from app.shared.infrastructure.database.connection import SessionLocal
from app.shared.infrastructure.persistence.user import User
from app.shared.infrastructure.persistence.address import Address
from app.shared.infrastructure.persistence.property import Property
from app.modules.inventory.infrastructure.persistence.animal import AnimalModel
from app.shared.infrastructure.persistence.email_verification_code import EmailVerificationCode

# Valid CPF Generator
def generate_valid_cpf():
    digits = [random.randint(0, 9) for _ in range(9)]
    s1 = sum(d * (10 - i) for i, d in enumerate(digits))
    r1 = (s1 * 10) % 11
    dig1 = 0 if r1 >= 10 else r1
    digits.append(dig1)
    s2 = sum(d * (11 - i) for i, d in enumerate(digits))
    r2 = (s2 * 10) % 11
    dig2 = 0 if r2 >= 10 else r2
    digits.append(dig2)
    return "".join(map(str, digits))

def run_integration_test():
    print("=" * 60)
    print("STARTING LIVE SUPABASE DATABASE INTEGRATION TEST")
    print("=" * 60)

    client = TestClient(app)
    db = SessionLocal()

    # Generate unique test user credentials
    test_id = secrets.token_hex(4)
    email = f"test.integration.{test_id}@aiboi.dev"
    password = "TestPassword123!"
    cpf = generate_valid_cpf()
    name = f"Test User {test_id}"
    
    print(f"[INFO] Generated Test Email: {email}")
    print(f"[INFO] Generated Test CPF: {cpf}")

    created_user_id = None
    created_address_id = None
    created_property_id = None
    created_animal_id = None

    try:
        # STEP 1: Request verification email code
        print("\n--- STEP 1: Sending verification code ---")
        response = client.post("/auth/signup/send-code", json={"email": email})
        if response.status_code != 200:
            raise RuntimeError(f"Failed to send code: {response.text}")
        
        response_data = response.json()
        verification_code = response_data.get("verification_code")
        if not verification_code:
            raise RuntimeError("Raw verification code was not returned by API. Ensure ENV=development.")
        
        print(f"[SUCCESS] Verification code sent and captured: {verification_code}")

        # STEP 2: Verify email code
        print("\n--- STEP 2: Verifying email code ---")
        response = client.post(
            "/auth/signup/verify-code",
            json={"email": email, "code": verification_code}
        )
        if response.status_code != 200:
            raise RuntimeError(f"Failed to verify code: {response.text}")
        print("[SUCCESS] Email verified successfully.")

        # STEP 3: Register test user
        print("\n--- STEP 3: Registering user ---")
        registration_payload = {
            "name": name,
            "email": email,
            "password": password,
            "cpf": cpf,
            "phone": "11999999999",
            "address": {
                "zip_code": "01001000",
                "state": "SP",
                "neighborhood": "Sé",
                "street_name": "Praça da Sé",
                "number": "100",
                "complement": "Apt 1"
            }
        }
        response = client.post("/auth/signup/register", json=registration_payload)
        if response.status_code != 201:
            raise RuntimeError(f"User registration failed: {response.text}")
        
        reg_data = response.json()
        created_user_id = reg_data["user_id"]
        created_address_id = reg_data["address_id"]
        print(f"[SUCCESS] User registered. ID: {created_user_id}, Address ID: {created_address_id}")

        # STEP 4: Login to obtain JWT token
        print("\n--- STEP 4: User Login ---")
        login_payload = {"email": email, "password": password}
        response = client.post("/auth/login", json=login_payload)
        if response.status_code != 200:
            raise RuntimeError(f"Login failed: {response.text}")
        
        login_data = response.json()
        token = login_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("[SUCCESS] Login successful. Access token obtained.")

        # Verify endpoint `/auth/me`
        print("\n--- STEP 4b: Verify /auth/me ---")
        response = client.get("/auth/me", headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch user profile: {response.text}")
        me_data = response.json()
        print(f"[SUCCESS] Profile authenticated: {me_data['name']} ({me_data['email']})")

        # STEP 5: Create a Property
        print("\n--- STEP 5: Creating Property ---")
        property_payload = {
            "name": f"Fazenda Integracao {test_id}",
            "size": 120.5,
            "property_type": "BEEF",
            "owner_id": created_user_id,
            "address_id": created_address_id
        }
        response = client.post("/properties/", json=property_payload, headers=headers)
        if response.status_code != 201:
            raise RuntimeError(f"Property creation failed: {response.text}")
        
        prop_data = response.json()
        created_property_id = prop_data["id_property"]
        print(f"[SUCCESS] Property created. ID: {created_property_id}")

        # STEP 6: Read Property
        print("\n--- STEP 6: Reading Property ---")
        response = client.get(f"/properties/{created_property_id}", headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Property read failed: {response.text}")
        read_prop = response.json()
        print(f"[SUCCESS] Property read back: {read_prop['name']}, Area: {read_prop['area']} hectares")

        # STEP 7: Update Property
        print("\n--- STEP 7: Updating Property ---")
        update_prop_payload = {
            "name": f"Fazenda Integracao Modificada {test_id}",
            "size": 150.0
        }
        response = client.put(f"/properties/{created_property_id}", json=update_prop_payload, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Property update failed: {response.text}")
        updated_prop = response.json()
        print(f"[SUCCESS] Property updated: {updated_prop['name']}, Area: {updated_prop['area']} hectares")

        # STEP 8: Create Animal under the Property
        print("\n--- STEP 8: Creating Animal ---")
        animal_ident = random.randint(100000, 999999)
        animal_payload = {
            "identification_number": animal_ident,
            "name": "Boi Integracao",
            "sex": "M",
            "breed": "Nelore",
            "animal_size": "GRANDE",
            "animal_life_status": "ATIVO",
            "animal_category": "Touro",
            "birth_date": "30/07/2022",
            "origin": "PROPRIEDADE",
            "notes": "Animal para teste de integracao"
        }
        response = client.post(f"/animals/?property_id={created_property_id}", json=animal_payload, headers=headers)
        if response.status_code != 201:
            raise RuntimeError(f"Animal creation failed: {response.text}")
        
        animal_data = response.json()
        created_animal_id = animal_data["id_animal"]
        print(f"[SUCCESS] Animal created. ID: {created_animal_id}, Ident: {animal_ident}")

        # STEP 9: Read Animal
        print("\n--- STEP 9: Reading Animal ---")
        response = client.get(f"/animals/{created_animal_id}?property_id={created_property_id}", headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Animal read failed: {response.text}")
        read_animal = response.json()
        print(f"[SUCCESS] Animal read back: {read_animal['name']}, Breed: {read_animal['breed']}, Status: {read_animal['animal_life_status']}")

        # STEP 10: Update Animal
        print("\n--- STEP 10: Updating Animal ---")
        update_animal_payload = {
            "name": "Boi Integracao Modificado",
            "notes": "Notes updated by integration test"
        }
        response = client.put(f"/animals/{created_animal_id}?property_id={created_property_id}", json=update_animal_payload, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Animal update failed: {response.text}")
        updated_animal = response.json()
        print(f"[SUCCESS] Animal updated: {updated_animal['name']}, Notes: {updated_animal['notes']}")

        # STEP 11: Delete Animal
        print("\n--- STEP 11: Deleting Animal ---")
        response = client.delete(f"/animals/{created_animal_id}?property_id={created_property_id}", headers=headers)
        if response.status_code != 204:
            raise RuntimeError(f"Animal deletion failed: {response.text}")
        print("[SUCCESS] Animal deleted via API.")

        # Verify Animal is deleted in DB
        animal_in_db = db.query(AnimalModel).filter(AnimalModel.id_animal == created_animal_id).first()
        assert animal_in_db is None, "Animal still exists in database!"
        print("[SUCCESS] Verified animal is completely gone from DB.")

        # STEP 12: Delete Property
        print("\n--- STEP 12: Deleting Property ---")
        response = client.delete(f"/properties/{created_property_id}", headers=headers)
        if response.status_code != 204:
            raise RuntimeError(f"Property deletion failed: {response.text}")
        print("[SUCCESS] Property deleted via API.")

        # Verify Property is deleted in DB
        property_in_db = db.query(Property).filter(Property.id_property == created_property_id).first()
        assert property_in_db is None, "Property still exists in database!"
        print("[SUCCESS] Verified property is completely gone from DB.")

        print("\n" + "=" * 60)
        print("LIFECYCLE TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:
        print("\n" + "!" * 60)
        print(f"TEST FAILED WITH ERROR: {str(e)}")
        traceback.print_exc()
        print("!" * 60)
        sys.exit(1)

    finally:
        # CLEANUP TEST USER & ADDRESS & CODES FROM DB
        print("\n--- CLEANUP AND TEARDOWN ---")
        try:
            if created_animal_id:
                db.query(AnimalModel).filter(AnimalModel.id_animal == created_animal_id).delete()
            if created_property_id:
                db.query(Property).filter(Property.id_property == created_property_id).delete()
            if created_user_id:
                db.query(User).filter(User.id_user == created_user_id).delete()
            if created_address_id:
                db.query(Address).filter(Address.id_address == created_address_id).delete()
            
            db.query(EmailVerificationCode).filter(EmailVerificationCode.email == email).delete()
            db.commit()
            print("[SUCCESS] Teardown clean-up complete: user, address, verification codes removed.")
        except Exception as cleanup_error:
            db.rollback()
            print(f"[WARNING] Failed to clean up database: {str(cleanup_error)}")
        finally:
            db.close()

if __name__ == "__main__":
    run_integration_test()
