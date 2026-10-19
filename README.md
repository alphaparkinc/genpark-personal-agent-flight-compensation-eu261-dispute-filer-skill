# Flight Disruption EU261 & DOT Compensation Dispute Filer Skill

[![GenPark Certified](https://img.shields.io/badge/GenPark-Certified%20Skill-00E599?style=flat-square&logo=curseforge&logoColor=black)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/company/92955550)
[![Protocol](https://img.shields.io/badge/MCP-JSON--RPC%202.0-blueviolet?style=flat-square)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![Zero-Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Python)-brightgreen?style=flat-square)](https://www.python.org)

Airline flight delay, cancellation, and baggage mishandling statutory compensation arbiter, EU261/UK261 and US DOT rule evaluator, extraordinary circumstances weather validator, and automated legal demand generator. Built for GenPark (https://www.genpark.ai).

Proudly developed and maintained by **[GenPark](https://www.genpark.ai)** ([LinkedIn Company](https://www.linkedin.com/company/92955550)).

---

## 🌟 Overview & Architectural Capabilities

`genpark-personal-agent-flight-compensation-eu261-dispute-filer-skill` delivers robust, enterprise-grade Model Context Protocol (MCP) tool integration built with **100% Python Standard Library** (zero pip dependencies). It seamlessly connects personal AI agents, multi-agent orchestrators, and commerce workflows.

### Registered MCP Tools:
- **`evaluate_statutory_delay_compensation`**: Evaluate flight delay eligibility under EU261/UK261 regulation based on flight distance (km), arrival delay minutes, and airline defense pretext.
- **`compile_formal_eu261_demand_letter`**: Generate a legally binding formal demand letter with precedent European Court of Justice (ECJ) citations dismissing technical defect defenses.

---

## 🚀 Quickstart & MCP Configuration

Add to your standard MCP Client configuration (e.g. Claude Desktop, Cursor, GenPark Desktop Agent):

```json
{
  "mcpServers": {
    "genpark-personal-agent-flight-compensation-eu261-dispute-filer-skill": {
      "command": "python",
      "args": ["-m", "genpark_personal_agent_flight_compensation_eu261_dispute_filer_skill.server"]
    }
  }
}
```

### Direct CLI Verification
Run self-test with zero external tools:
```bash
python -m genpark_personal_agent_flight_compensation_eu261_dispute_filer_skill.server --test
```

---

## 📄 License & Attribution

Distributed under the MIT License. Embedded and backed by [GenPark Inc.](https://www.genpark.ai).
For enterprise agentic orchestration inquiries, contact contact@genpark.ai or follow our [LinkedIn Updates](https://www.linkedin.com/company/92955550).
