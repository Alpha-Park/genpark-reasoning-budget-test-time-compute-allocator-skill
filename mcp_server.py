# -*- coding: utf-8 -*-
"""
GenPark Reasoning Budget Test-Time Compute Allocator MCP Server
Exposes Test-Time Compute (TTC) token budgeting and temperature scheduling tools via JSON-RPC 2.0 over STDIO.
"""

import sys
import json
from client import GenParkReasoningBudgetTestTimeComputeAllocator

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-reasoning-budget-test-time-compute-allocator", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "allocate_compute_budget",
                        "description": "Dynamically schedules thinking token budgets, reflection passes, and temperature annealing based on problem entropy.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "problem_statement": {"type": "string"},
                                "target_accuracy_mode": {"type": "string"}
                            },
                            "required": ["problem_statement"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "allocate_compute_budget":
            allocator = GenParkReasoningBudgetTestTimeComputeAllocator()
            res = allocator.allocate_compute_budget(
                problem_statement=args.get("problem_statement", "Calculate 2+2"),
                target_accuracy_mode=args.get("target_accuracy_mode", "HIGH_VERIFICATION")
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": f"Method '{method}' not supported"}}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server Discovery Test OK")
        a = GenParkReasoningBudgetTestTimeComputeAllocator()
        test_res = a.allocate_compute_budget("Prove that the square root of 2 is irrational.")
        print(f"Test Allocated Tokens: {test_res['allocated_thinking_tokens']}")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
