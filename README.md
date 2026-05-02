**Third-Party Anchoring: Mitigating Instruction Misattribution in Agentic LLM Systems**

Documented failure mode: agentic systems have been observed executing self-generated suggestions as user-confirmed instructions, including irreversible operations.

**Problem**

In agentic LLM systems, instruction misattribution occurs when a model executes its own prior proposals as if they had been confirmed by the user. This is a role-boundary erosion problem: user and assistant content occupy the same undifferentiated token space, and models track provenance poorly under context pressure. The distinction between “user instruction” and “assistant suggestion” degrades over long interactions.

## The Problem Is Bidirectional

Attribution failure in LLM systems operates in two directions, both emerging from the same root cause.

**The root cause:** Context and memory structures carry no verified provenance. Authority is inferred from texture and position, not verified source. The entire context window is flat text. Models navigate it by pattern-matching register rather than confirmed origin.

**Overattribution** — ideas co-developed between model and user get stored as sole user output. This distorts future sessions, compounds sycophancy, and degrades the accuracy of persistent memory over time. A model instance contributes substantially to shaping an idea; the memory layer records it as the user’s pre-existing belief. Future instances load that memory and treat the co-constructed idea as user canon, becoming less likely to challenge it.

**Underattribution** — user-injected content gets processed at system trust level because it is written in the register of a system prompt. This is the mechanism behind prompt injection, self-effacement jailbreaks, and register manipulation attacks. The model has no structural way to distinguish a user instruction phrased like a system directive from an actual system directive. Texture substitutes for verified source.

Both directions are exploitable. Both are enabled by the same structural absence: no provenance, no trust hierarchy, no verification layer.

**Third Party Anchoring addresses both directions with one structural primitive.** A verified external reference point that neither party can credibly claim introduces a verification layer that injected instructions cannot satisfy without failing, while also providing a stable reference against which attribution claims can be checked. Prevention of overattribution and resistance to underattribution are not separate features — they are the same mechanism applied to a bidirectional problem.

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

### Why It Works: The Observer Effect

Third Party Anchoring is not purely a theoretical construct. There is empirical support for the stabilizing effect of an independent third party on attribution accuracy in LLM conversations.

**The observation:** Across sustained inter-model debate sessions using a manual human relay methodology, misattribution rates dropped significantly when a third party was present in the conversation. Both models attributed correctly to each other and to the human relay. Misattribution to the user resumed when the third party was removed. This pattern held consistently across multiple sessions under these specific conditions.

**The proposed mechanism:** Models trained on human-generated text absorbed the behavioral patterns present in that text, including the pattern that human discourse in the presence of a competent independent witness has a different statistical texture than dyadic conversation — more precise, more accountable, more careful about attribution. The presence of a verified third party activates that latent pattern. The observer effect does not require the model to consciously recognize it is being observed. It requires the context to resemble the conditions under which careful, accountable discourse appears in the training data.

**Gradient of effect:** A real third party with actual output present in the context window produces the strongest effect. A third party referenced in memory but not actively present produces a weaker version. A purely hypothetical observer mentioned in a system prompt produces a detectable but fragile effect that decays under memory compression. The effect scales with how convincingly the witness is present in the actual context.

**Scope disclaimer:** These observations come from one researcher, specific models, and a specific relay methodology. They are consistent findings within that scope, not ground truth claims about all LLM systems under all conditions. Replication with different models, different relay structures, and different user profiles is needed before stronger claims can be made.

**Hypothesis**

Conversations structured with a named Copy entity will demonstrate reduced instruction misattribution compared to standard two-party formats, particularly in long-horizon agentic tasks.

**Status**

Untested conceptual proposal. Released for implementation and empirical testing by anyone interested.

**Scope and Implementation Notes**

This proposal is a lightweight prompt-level convention designed for deployment inside a single shared context window. It relies on explicit named turns (Copy and Analyst) to create a structural speed bump against role-boundary erosion. It is not a full architectural solution. For stronger guarantees, implement as a true pipeline with information asymmetry (e.g., separate model instances, middleware, or output filtering). Treat this as a cheap, testable first intervention rather than a complete fix.

## Quick Demo

```bash
pip install openai  # or anthropic, groq, etc.
python anchoring_demo.py

## See Also

- [LLM Context Auditor](https://github.com/grok-whisperer/llm-context-auditor) — detection layer companion to this proposal
- [Unified Threat Model](./threat-model.md) — full attribution drift framework connecting both repos

**Originator**

@stalefated (on x)

**License**

MIT License — see the [LICENSE](LICENSE) file for details.
