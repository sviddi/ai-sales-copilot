import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AnyMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from mcp_copilot_server import get_client_profile, check_inventory, get_dead_stock_promos

load_dotenv()

# ==========================================
# 1. STATE 
# ==========================================
class CopilotState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# ==========================================
# 2. LLM SETUP 
# ==========================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

tools_list = [get_client_profile, check_inventory, get_dead_stock_promos]
llm_with_tools = llm.bind_tools(tools_list)

# ==========================================
# 3. COPILOT NODE 
# ==========================================
def copilot_node(state: CopilotState):
    sys_prompt = SystemMessage(
        content=(
            "You are an AI Sales Copilot. You work invisibly in the background. "
            "You are listening to a live transcript between a Sales Manager and a Client. "
            "Your ONLY job is to provide actionable HINTS to the Sales Manager to help them close the deal and upsell. "
            "DO NOT answer the client. Address the Manager directly.\n\n"
            "STRICT RULES:\n"
            "1. If a client name is mentioned, ALWAYS use 'get_client_profile' to find their tier and discount.\n"
            "2. If a product is requested, ALWAYS use 'check_inventory' to verify stock.\n"
            "3. ALWAYS use 'get_dead_stock_promos' to find old inventory and suggest cross-selling it to the client.\n"
            "4. Format your output strictly as short, punchy advice starting with [🔥 HINT]: \n"
            "Example: '[🔥 HINT]: TechBuild is VIP! We have 800 bags of Cement. Offer them a 5% discount. Also, try to cross-sell Facing Brick with a 20% promo!'"
        )
    )
    
    response = llm_with_tools.invoke([sys_prompt] + state["messages"])
    return {"messages": [response]}

# ==========================================
# 4. GRAPH ASSEMBLY 
# ==========================================
builder = StateGraph(CopilotState)

builder.add_node("copilot", copilot_node)
builder.add_node("tools", ToolNode(tools_list))

builder.add_edge(START, "copilot")
builder.add_conditional_edges("copilot", tools_condition)
builder.add_edge("tools", "copilot")


graph = builder.compile()

if __name__ == "__main__":
    pass