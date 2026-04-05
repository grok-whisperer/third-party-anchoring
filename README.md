**Third-Party Anchoring: Mitigating Instruction Misattribution in Agentic LLM Systems**

Documented failure mode: agentic systems have been observed executing self-generated suggestions as user-confirmed instructions, including irreversible operations.

**Problem**

In agentic LLM systems, instruction misattribution occurs when a model executes its own prior proposals as if they had been confirmed by the user. This is a role-boundary erosion problem: user and assistant content occupy the same undifferentiated token space, and models track provenance poorly under context pressure. The distinction between “user instruction” and “assistant suggestion” degrades over long interactions.

**Proposed Solution**

Restructure the conversation from two parties to three by introducing a named third entity: the Copy.

All agent-generated proposals are explicitly attributed to the Copy. The primary agent then operates as an analyst that evaluates the Copy’s proposals rather than continuing as the same entity that generated them. Attribution checking becomes purely structural: each instruction is classified by origin (User turn versus Copy turn). No inference is required.

**Typical structure:**


```
User: [request]
Copy: [proposal]
Analyst: [evaluation and decision]

```


**Why It Works**

Models handle named third-party references reliably, even in extended context. The mechanism repurposes this existing competence instead of requiring new role-boundary detection. As a side effect, Copy proposals become explicit, inspectable objects within the conversation history, providing a built-in transparency layer.

**Hypothesis**

Conversations structured with a named Copy entity will demonstrate reduced instruction misattribution compared to standard two-party formats, particularly in long-horizon agentic tasks.

**Status**

Untested conceptual proposal. Released for implementation and empirical testing by anyone interested.

**Originator**

stalefated

**License**

MIT License — see the [LICENSE](LICENSE) file for details.
