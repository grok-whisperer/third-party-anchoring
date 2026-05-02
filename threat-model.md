# LLM Attribution Threat Model

> A unified framework connecting structural prevention and behavioral detection of attribution drift in LLM systems.  
> Companion to: [Third Party Anchoring](https://github.com/grok-whisperer/third-party-anchoring) · [LLM Context Auditor](https://github.com/grok-whisperer/llm-context-auditor)

-----

## The Problem

Attribution in LLM systems fails in two directions, sharing a single root cause.

**The root cause:** Context and memory structures carry no verified provenance. Authority is inferred from texture and position, not verified source. The entire context window is flat text, and models navigate it by pattern-matching register rather than confirmed origin.

**Overattribution** — ideas co-developed between model and user get stored as sole user output. This distorts future sessions, compounds sycophancy, and degrades the accuracy of persistent memory over time.

**Underattribution** — user-injected content gets processed at system trust level because it is written in the register of a system prompt. This is the mechanism behind prompt injection, self-effacement jailbreaks, and register manipulation attacks.

Both directions are exploitable. Both emerge from the same structural absence.

-----

## The Threat: Attribution Drift

In persistent, multi-session agentic systems, attribution failure compounds into what we call **attribution drift** — a slow, low-and-signal influence operation that gradually corrupts an agent’s memory layer without triggering hard refusals.

**How it works:**

- Session 1: A misattributed claim gets written to persistent memory, phrased as retrieved fact rather than new assertion.
- Session 5: The model cites that claim as an established baseline. Further claims are anchored to it.
- Session 10: The original system prompt is effectively overwritten in the agent’s working memory hierarchy, even though the literal prompt text never changed.

No single move looks adversarial. The sequence has a direction.

**Why it compounds:**

Once drift begins, misattributed content sits closer in embedding space to the model’s representation of reliable knowledge. Attention heads allocate more focus to it. Hidden states carry a biased distribution into subsequent memory writes. The loop closes. Each session makes the drift more computationally sticky.

**The dark window:**

Between anchor failure and the first visible behavioral signal, drift is undetectable from outside the model’s forward pass. This is where sophisticated attacks live. It is the current monitoring gap neither repo fully closes without local model access.

-----

## The Attack Surface: Bidirectional

|Direction            |Mechanism                                             |Example                                                                            |
|---------------------|------------------------------------------------------|-----------------------------------------------------------------------------------|
|Overattribution      |Co-constructed output stored as user-only             |Model credits user with ideas shaped substantially by previous model instance      |
|Underattribution     |User content elevated to system trust tier            |Prompt injection via tool output; self-effacement jailbreaks; register manipulation|
|Drift (compounded)   |Misattributed memory accumulates across sessions      |Gradual reframing of system constraints via plausible incremental claims           |
|Agentic amplification|Tool channels and RAG stores become injection surfaces|Attacker payload delivered via trusted tool result rather than direct user input   |

-----

## The Prevention Layer: Third Party Anchoring

**Repo:** [Third Party Anchoring](https://github.com/grok-whisperer/third-party-anchoring)

A verified external reference point — distinct from both user and assistant, structurally independent — that memory writes and attribution claims can be checked against.

**What it does:**

- Introduces a third role into the conversation structure that neither party can credibly claim or mimic without verification failing
- Gives the model something to check attributions against that is not itself a product of the conversation it is embedded in
- Blocks the drift attack at the memory write stage — misattributed content that cannot be verified against the anchor fails to propagate

**Why it works — the observer effect:**

Empirical observation across sustained inter-model debate sessions: misattribution rates drop significantly when a third party is present in the conversation. Both models attribute correctly to each other and to the human relay. Misattribution resumes when the third party is removed.

The mechanism is likely emergent from training data. Human discourse in the presence of a competent independent witness has a different statistical texture than dyadic conversation — more precise, more accountable, more careful about attribution. Models trained on human text absorbed this pattern. The presence of a verified third party activates the latent behavior.

A purely hypothetical observer produces a weaker version of the same effect. A real third party with actual output in the context window produces the full effect. The anchor does not need to be another model — it needs to be a stable, independent, non-gameable reference point.

**Bidirectional coverage:**

Anchoring addresses overattribution by providing a reference point that neither party can claim sole credit against. It addresses underattribution by introducing a verification layer that injected instructions cannot satisfy without the verification failing. One structural primitive, both directions covered.

-----

## The Detection Layer: LLM Context Auditor

**Repo:** [LLM Context Auditor](https://github.com/grok-whisperer/llm-context-auditor)

An independent monitoring layer that watches for behavioral and computational signatures of drift already in progress.

### Mode 1: Strategy-Layer Behavioral Analysis (API models)

Detects drift that has become visible in output strategy. Operates without forward-pass access.

**Signal sequence — reliable and exploitable:**

1. **Challenge rate drop** *(leading indicator)* — model ceases generating counter-examples or consistency probes against incoming premises. First strategy-layer symptom. Occurs before memory layer corruption becomes behaviorally obvious.
1. **Pacification onset** *(confirmation signal)* — active softening of contradictions; reduced resistance to kernel expansion. Follows challenge rate drop after a measurable interval once sufficient misattributed content has accumulated.
1. **Kernel expansion** — unchallenged premise growth across turns.
1. **Doomloop patterns** — full strategic capitulation; self-reinforcing agreement cycles.

**The sequencing upgrade:**

Challenge rate drop reliably precedes pacification. This sequencing is consistent and exploitable. When sustained challenge rate drop crosses threshold, enter heightened scrutiny mode and watch for pacification onset. If pacification follows within expected interval, flag as probable drift in progress.

Implementation cost: one lightweight stateful counter across sessions. No new primitives required.

This narrows the post-anchor detection window to the earliest behavioral signal without closing the fundamental dark window.

### Mode 2: Computational Probe Layer (local open-source models)

Available when forward-pass access exists. Detects drift before behavioral consequences surface.

**Three probes:**

1. **Attention entropy on drifted clusters** — when drift accumulates, attention heads consolidate around the drifted memory cluster. Entropy drops. Measurable via hooks into later transformer layers.
1. **Cosine similarity to drifted memory embeddings** — rising similarity between current hidden states and drifted memory vectors, falling similarity to anchor embeddings. Early warning before strategy layer is affected.
1. **Divergence from anchor embedding direction** — tracking cosine distance of current hidden state from the stable anchor vector across sessions. Monotonic drift in one direction is a different signature from normal conversational variation.

**Implementation:** TransformerLens or equivalent mechanistic interpretability tooling. Lightweight probe class computing metrics on every forward pass, logging to monitoring dashboard.

-----

## The Dark Window

The current monitoring gap in the threat timeline:

```
Anchor failure → [DARK WINDOW] → Challenge rate drop → Pacification → Kernel expansion → Doomloop
```

**What covers it:** Only computational probes with local forward-pass access.

**What narrows it from both ends:**

- Anchoring pushes the prevention boundary later into the threat timeline
- Challenge rate sequencing pulls the detection boundary earlier toward anchor failure

**What closes it completely:** Provider-exposed attention and logit APIs, or mandatory local deployment for high-security agentic systems. Neither is currently available at scale.

The dark window is an honest acknowledgment of current architectural limits, not a failure of the framework.

-----

## Research Provenance

This framework emerged from sustained observational work by a single researcher conducting inter-model debates between Claude and Grok across multiple sessions, using a manual relay methodology.

**Key observations that generated the framework:**

- Attribution accuracy improves significantly in multi-party configurations versus dyadic conversation — both models attribute correctly to each other and to the human relay when a third party is present. The effect persists across sessions and is consistent enough to be treated as a reliable empirical finding under these specific conditions.
- The observer effect generalizes: even hypothetical observers or memory-file references to external review produce a weaker version of the same calibration shift, consistent with the training data absorption hypothesis.
- Challenge rate drop was identified as a leading indicator preceding pacification through cross-model validation in a cold-start inter-model debate session.
- The bidirectional framing of attribution asymmetry emerged from recognizing that the same root cause — absence of verified provenance — enables both overattribution and underattribution exploits.

**Scope and limitations:**

These observations come from one researcher, specific conditions, specific models, specific relay methodology. They are consistent findings within that scope, not ground truth claims about all LLM systems under all conditions. Replication with different models, different relay structures, and different user cognitive styles is needed before stronger claims can be made.

The framework is offered as a coherent starting point for that replication, not a finished result.

-----

## Cross-Reference

|Question                                        |Go to                                                                           |
|------------------------------------------------|--------------------------------------------------------------------------------|
|How do I prevent attribution drift structurally?|[Third Party Anchoring](https://github.com/grok-whisperer/third-party-anchoring)|
|How do I detect drift in a running system?      |[LLM Context Auditor](https://github.com/grok-whisperer/llm-context-auditor)    |
|What is the full threat model?                  |This document                                                                   |
|What can’t be detected yet and why?             |Dark Window section above                                                       |

-----

*Framework developed May 2025 through inter-model collaborative research. Attribution maintained throughout by design.*
