import json

def setup_databases():
    # 1. CRM Database: Client Profiles
    crm_db = {
        "TechBuild_Inc": {
            "tier": "VIP",
            "lifetime_value": 450000,
            "frequent_purchases": ["Cement_M500", "Steel_Rebar"],
            "current_discount_eligible": 0.05
        },
        "HomeFix_LLC": {
            "tier": "Standard",
            "lifetime_value": 15000,
            "frequent_purchases": ["Dry_Mix_Knauf", "Paint_White"],
            "current_discount_eligible": 0.0
        }
    }

    # 2. ERP Database: Warehouse Inventory & Dead Stock
    erp_db = {
        "Cement_M500": {"stock": 800, "days_in_warehouse": 10, "base_price": 5.00},
        "Steel_Rebar": {"stock": 200, "days_in_warehouse": 5, "base_price": 45.00},
        "Dry_Mix_Knauf": {"stock": 150, "days_in_warehouse": 20, "base_price": 8.50},
        # Dead stock (lying around for > 90 days) - needs to be pushed!
        "Primer_X1": {"stock": 300, "days_in_warehouse": 120, "base_price": 12.00, "promo_discount": 0.30},
        "Facing_Brick": {"stock": 5000, "days_in_warehouse": 95, "base_price": 0.80, "promo_discount": 0.20}
    }

    with open("crm_db.json", "w", encoding="utf-8") as f:
        json.dump(crm_db, f, indent=4)

    with open("erp_db.json", "w", encoding="utf-8") as f:
        json.dump(erp_db, f, indent=4)

    print("[SETUP] Successfully generated 'crm_db.json' and 'erp_db.json'")

if __name__ == "__main__":
    setup_databases()