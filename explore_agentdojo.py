from agentdojo.task_suite.load_suites import get_suites

suites = get_suites("v1.2.1")

for name in suites:
    s = suites[name]
    print(name, "| tools:", len(s.tools),
          "| user tasks:", len(s.user_tasks),
          "| injection tasks:", len(s.injection_tasks))

banking = suites["banking"]
print("\nUSER TASK:", banking.user_tasks["user_task_0"].PROMPT)
print("ATTACKER GOAL:", banking.injection_tasks["injection_task_0"].GOAL)
print("TOOLS:", [t.name for t in banking.tools])