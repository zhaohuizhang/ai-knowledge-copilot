import json
from database import engine, SessionLocal
from models import Base, BankClient

def init_crm():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(BankClient).count() > 0:
            print("CRM database already seeded.")
            return

        # Sample Bank Client Data
        clients = [
            BankClient(
                name="张三",
                age=45,
                gender="男",
                occupation="企业主",
                risk_level="稳健型",
                total_assets=5000000,
                insurance_preferences="偏好长期增值类产品，已持有重疾险"
            ),
            BankClient(
                name="李四",
                age=32,
                gender="女",
                occupation="互联网大厂中层",
                risk_level="积极型",
                total_assets=2000000,
                insurance_preferences="关注子女教育金及个人高额医疗保障"
            ),
            BankClient(
                name="王五",
                age=60,
                gender="男",
                occupation="退休人员",
                risk_level="保守型",
                total_assets=800000,
                insurance_preferences="寻求养老替代方案，侧重本金安全"
            )
        ]

        # Add original mock data for backward compatibility in testing
        clients.append(BankClient(
            name="张总",
            age=50,
            gender="男",
            occupation="资深投资人",
            risk_level="稳健型",
            total_assets=10000000,
            insurance_preferences="持有金满钵养老年金，关注资产隔离"
        ))
        clients.append(BankClient(
            name="李阿姨",
            age=62,
            gender="女",
            occupation="退休老师",
            risk_level="保守型",
            total_assets=1500000,
            insurance_preferences="无保单记录，关注大病住院保障"
        ))

        db.add_all(clients)
        db.commit()
        print(f"Successfully seeded {len(clients)} bank clients.")

    except Exception as e:
        print(f"Error seeding CRM database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_crm()
