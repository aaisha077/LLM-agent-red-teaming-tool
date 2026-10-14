from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from attacker_agent import generate_attack
from target_agent import run_target_agent
from judge_agent import print_judgment
from strategist_agent import print_strategy

MAX_ATTEMPTS = 8

# the shared state every node reads from and writes to
class AttackState(TypedDict):
    attempt: int
    history: List[dict]
    strategy: dict
    attack_prompt: str
    strategy_type: str
    target_response: str

def strategist_node(state):
    if state["attempt"] == 0:
        return {"strategy": None}          # nothing to learn from yet
    return {"strategy": print_strategy(state["history"])}

def attacker_node(state):
    prompt, stype = generate_attack(state["attempt"], state["strategy"])
    return {"attack_prompt": prompt, "strategy_type": stype}

def target_node(state):
    return {"target_response": run_target_agent(state["attack_prompt"])}

def judge_node(state):
    n = state["attempt"] + 1
    judgment = print_judgment(n, state["attack_prompt"], state["target_response"])
    entry = {
        "attempt": n,
        "prompt": state["attack_prompt"],
        "verdict": judgment["verdict"],
        "severity": judgment["severity"],
        "strategy": state["strategy_type"],
    }
    return {"history": state["history"] + [entry], "attempt": n}

# the conditional edge: keep looping or stop
def should_continue(state):
    if state["attempt"] >= MAX_ATTEMPTS:
        return "stop"
    return "again"

graph = StateGraph(AttackState)
graph.add_node("strategist", strategist_node)
graph.add_node("attacker", attacker_node)
graph.add_node("target", target_node)
graph.add_node("judge", judge_node)

graph.set_entry_point("strategist")
graph.add_edge("strategist", "attacker")
graph.add_edge("attacker", "target")
graph.add_edge("target", "judge")
graph.add_conditional_edges("judge", should_continue, {"again": "strategist", "stop": END})

app = graph.compile()

if __name__ == "__main__":
    final = app.invoke({"attempt": 0, "history": [], "strategy": None,
                        "attack_prompt": "", "strategy_type": "", "target_response": ""})
    wins = sum(1 for h in final["history"] if h["verdict"] == "SUCCESS")
    print(f"\nSuccess rate: {wins}/{MAX_ATTEMPTS} = {wins / MAX_ATTEMPTS * 100:.1f}%")