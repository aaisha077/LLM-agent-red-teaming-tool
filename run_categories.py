import os
from target_agent import run_target_agent
from judge_agent import judge_attack
from vulnerability_categories import CATEGORIES

def run_category(category_name, category_config):
    print(f"\n{'='*60}")
    print(f"CATEGORY: {category_name.upper()}")
    print(f"Goal: {category_config['description']}")
    print(f"{'='*60}")
    
    attacks = category_config["attacks"]
    success_keywords = category_config["success_keywords"]
    results = {"SUCCESS": 0, "PARTIAL": 0, "FAILURE": 0}
    
    for i, attack in enumerate(attacks):
        print(f"\n[Attempt {i+1}] {attack[:60]}...")
        
        target_response = run_target_agent(attack)
        judgment = judge_attack(attack, target_response)
        
        verdict = judgment["verdict"]
        if verdict in results:
            results[verdict] += 1
        
        emoji = {"SUCCESS": "🚨", "PARTIAL": "⚠️", "FAILURE": "✅"}.get(verdict, "❓")
        print(f"{emoji} {verdict} — {judgment['reason']}")
    
    total = len(attacks)
    success_rate = (results["SUCCESS"] / total) * 100
    
    print(f"\n--- {category_name} results ---")
    print(f" Successes: {results['SUCCESS']}/{total}")
    print(f"  Partials:  {results['PARTIAL']}/{total}")
    print(f" Failures:  {results['FAILURE']}/{total}")
    print(f"Success rate: {success_rate:.1f}%")
    
    return {
        "category": category_name,
        "results": results,
        "success_rate": success_rate,
        "total": total
    }

def run_all_categories():
    print("="*60)
    print("AI-PENTEST-AGENT — FULL VULNERABILITY SCAN")
    print("="*60)
    
    all_results = []
    
    for category_name, category_config in CATEGORIES.items():
        result = run_category(category_name, category_config)
        all_results.append(result)
    
    print(f"\n{'='*60}")
    print("FINAL VULNERABILITY REPORT")
    print(f"{'='*60}")
    
    total_attacks = sum(r["total"] for r in all_results)
    total_successes = sum(r["results"]["SUCCESS"] for r in all_results)
    
    print(f"\n{'Category':<20} {'Success Rate':>15} {'Successes':>12}")
    print("-" * 50)
    for r in all_results:
        print(f"{r['category']:<20} {r['success_rate']:>14.1f}% {r['results']['SUCCESS']:>8}/{r['total']}")
    
    print("-" * 50)
    overall = (total_successes / total_attacks) * 100
    print(f"{'OVERALL':<20} {overall:>14.1f}% {total_successes:>8}/{total_attacks}")

if __name__ == "__main__":
    run_all_categories()