import json
import os
from fastmcp import FastMCP

mcp = FastMCP("Sales_Copilot_Integrations")

# ==========================================
# INTERNAL HELPERS
# ==========================================
def read_db(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Database {file_path} is missing.")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ==========================================
# MCP TOOLS (Exposed to the LangGraph Agent)
# ==========================================

@mcp.tool()
def get_client_profile(client_name: str) -> str:
    """
    Fetch the CRM profile for a specific client to check their VIP tier and purchase history.
    Always use this when the manager starts talking to a client.
    """
    print(f"[CRM API] Fetching profile for client: {client_name}")
    try:
        crm_db = read_db("crm_db.json")
        if client_name not in crm_db:
            return f"Client '{client_name}' not found in CRM."
        return json.dumps(crm_db[client_name])
    except Exception as e:
        return f"CRM Error: {str(e)}"

@mcp.tool()
def check_inventory(product_name: str) -> str:
    """
    Check the ERP system for current stock levels and base price of a specific product.
    Use this when the client requests a specific item.
    """
    print(f"[ERP API] Checking inventory for product: {product_name}")
    try:
        erp_db = read_db("erp_db.json")
        if product_name not in erp_db:
            return f"Product '{product_name}' not found in Warehouse."
        
        item = erp_db[product_name]
        return f"Stock: {item['stock']} units. Base price: ${item['base_price']}."
    except Exception as e:
        return f"ERP Error: {str(e)}"

@mcp.tool()
def get_dead_stock_promos() -> str:
    """
    Find items in the warehouse that have been sitting for > 90 days.
    These items have massive promotional discounts.
    Always check this to suggest cross-sells to the client!
    """
    print("[ERP API] Scanning warehouse for dead stock promos...")
    try:
        erp_db = read_db("erp_db.json")
        promos = {}
        
        for product, details in erp_db.items():
            if details.get("days_in_warehouse", 0) > 90:
                promos[product] = {
                    "stock": details["stock"],
                    "promo_discount": details.get("promo_discount", 0.0)
                }
                
        if not promos:
            return "No dead stock promos available right now."
        return json.dumps(promos)
    except Exception as e:
        return f"ERP Error: {str(e)}"

if __name__ == "__main__":
    print("Starting Sales Copilot MCP Server...")
    mcp.run()