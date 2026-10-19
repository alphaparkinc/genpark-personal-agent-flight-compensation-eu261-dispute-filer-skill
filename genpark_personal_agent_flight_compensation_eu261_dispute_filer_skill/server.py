# -*- coding: utf-8 -*-
"""Model Context Protocol (MCP) Server for Flight Disruption EU261 & DOT Compensation Dispute Filer Skill
Powered by GenPark (https://www.genpark.ai).
"""
import sys
import json
import logging
from .core import *

TOOLS_METADATA = [
  {
    "name": "evaluate_statutory_delay_compensation",
    "description": "Evaluate flight delay eligibility under EU261/UK261 regulation based on flight distance (km), arrival delay minutes, and airline defense pretext.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "flight_number": {
          "type": "string"
        },
        "departure_airport_iata": {
          "type": "string"
        },
        "arrival_airport_iata": {
          "type": "string"
        },
        "flight_distance_km": {
          "type": "number"
        },
        "arrival_delay_minutes": {
          "type": "integer"
        },
        "airline_claimed_reason": {
          "type": "string",
          "enum": [
            "technical_defect",
            "crew_shortage",
            "air_traffic_control",
            "severe_weather",
            "strike"
          ]
        }
      },
      "required": [
        "flight_number",
        "flight_distance_km",
        "arrival_delay_minutes",
        "airline_claimed_reason"
      ]
    }
  },
  {
    "name": "compile_formal_eu261_demand_letter",
    "description": "Generate a legally binding formal demand letter with precedent European Court of Justice (ECJ) citations dismissing technical defect defenses.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "passenger_name": {
          "type": "string"
        },
        "booking_reference": {
          "type": "string"
        },
        "airline_legal_entity": {
          "type": "string"
        },
        "claim_amount_eur": {
          "type": "number"
        }
      },
      "required": [
        "passenger_name",
        "booking_reference",
        "airline_legal_entity",
        "claim_amount_eur"
      ]
    }
  }
]

def handle_rpc(request_str: str) -> str:
    try:
        req = json.loads(request_str)
    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None})
    
    msg_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-flight-compensation-eu261-dispute-filer-skill",
                    "version": "1.0.0",
                    "vendor": "GenPark (https://www.genpark.ai)"
                }
            }
        })

    if method == "tools/list":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": TOOLS_METADATA}
        })

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        func = globals().get(tool_name)
        if not func or not callable(func):
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}
            })
        
        try:
            call_res = func(**arguments)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(call_res, ensure_ascii=False, indent=2)}
                    ]
                }
            })
        except Exception as err:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32000, "message": f"Execution error: {str(err)}"}
            })

    return json.dumps({
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unhandled method '{method}'"}
    })

def run_self_test():
    print(f"=== Running Self Test for genpark-personal-agent-flight-compensation-eu261-dispute-filer-skill ===")
    init_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})))
    assert "result" in init_res, "Initialize failed"
    print("[PASS] MCP initialize")

    list_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})))
    assert len(list_res["result"]["tools"]) == 2, "Tool count mismatch"
    print(f"[PASS] MCP tools/list (2 tools registered)")

    # Execute smoke test for each tool

    call1 = json.loads(handle_rpc(json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "evaluate_statutory_delay_compensation",
            "arguments": {
                "flight_number": "BA178",
                "departure_airport_iata": "JFK",
                "arrival_airport_iata": "LHR",
                "flight_distance_km": 5540.0,
                "arrival_delay_minutes": 260,
                "airline_claimed_reason": "technical_defect"
            }
        }
    })))
    assert "result" in call1, "Call1 failed"
    print("[PASS] Tool smoke test: evaluate_statutory_delay_compensation")

    print("[ALL TESTS PASSED] Self-test verified successfully.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        success = run_self_test()
        sys.exit(0 if success else 1)
    
    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
