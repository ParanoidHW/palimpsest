# Evidence And Readability Contract

## Evidence Levels

Use these exact classes in ledgers and prose:

| Class | Supports | Does not support by itself |
| --- | --- | --- |
| `paper` | Proposed mechanism, stated assumptions, reported experiments | Current framework behavior |
| `official-doc` | Supported public behavior at the documented version | Undocumented internal execution |
| `pinned-source` | Behavior visible at one immutable commit | Performance or behavior at other revisions |
| `measurement` | Observed result under a recorded setup | General causal claims outside that setup |
| `analysis-derived` | Explicit synthesis across cited evidence | A claim attributed to any one source |

Give each claim an evidence ID. When evidence disagrees, preserve the conflict and version boundary instead of averaging it away.

## Source Records

Each `sources.jsonl` object must include `id`, `type`, `title`, `url`, and `accessed`. Repository records also require `repository` and a 40-character lowercase `commit`. Optional fields include `version`, `authors`, `published`, `license`, and `notes`.

Each implementation trace must include a unique `id`, framework, method, source evidence ID, lifecycle phase, and five non-empty hops: `config`, `entry_api`, `runtime`, `collective`, `tensor_layout`. Every hop requires `path`, `symbol`, `lines`, and `behavior`; `config` may use a configuration file path and key as its symbol. The behavior must state what changes, not merely repeat the symbol name.

## Explanation Order

For each new concept, use this order:

1. One ordinary-language sentence.
2. Strict definition and scope.
3. Concrete tensor or state example.
4. Framework symbol and evidence ID.

Expand abbreviations locally at first use even when the glossary defines them. Keep glossary entries canonical and include term, abbreviation, aliases, plain explanation, strict definition, commonly confused concepts, and source IDs.

## Tensor Walkthrough Rubric

A walkthrough passes only when it gives:

- named global tensor/state and numeric pre-partition shape;
- partition axis and world size;
- numeric rank-local shape and ownership for at least two ranks or a general rank formula;
- local operation and its input/output shapes;
- collective payload, senders, receivers, reduction/reordering rule, and output shape;
- why the output equals the unpartitioned semantics;
- communication volume, persistent memory, temporary buffers, and buffer lifetime;
- a concrete invalid shape, missing collective, or incompatible composition example.

## Formula Rubric

Follow every displayed formula with a paragraph beginning with `公式解释：` or `Formula explanation:`. Name every symbol and state which engineering question the formula answers. A formula without this explanation is an error.

## Source Trace Rubric

For every hop, answer both “where?” and “what happens?”. A list such as `Config -> Engine -> Layer -> all_reduce` fails because identifiers replace behavior. A valid chain explains that the config chooses a group size, the entry API constructs a group, the runtime partitions a dimension, the collective exchanges a named payload, and the resulting rank-local/global layout.

## Lifecycle Rubric

Address `training`, `prefill`, and `decode` separately or mark each `not-applicable` with a reason. Training must discuss forward, backward, and optimizer state. Prefill must discuss token shape, scheduling, and KV-cache population. Decode must discuss one/few-token steps, cache reads/appends, dynamic batching, and communication frequency.

## Human Acceptance

Ask an engineer unfamiliar with the framework to answer:

1. What tensor or state is split?
2. What does each device own?
3. Where and why is communication required?
4. Why is the distributed result mathematically correct?
5. Which memory or compute is saved?
6. What communication, buffering, recomputation, or scheduling cost is added?
7. Which configuration and source entry begin the implementation?

Any answer that depends on unexplained framework jargon fails. Long sentences and high term density are warnings: rewrite only when human review confirms they impede the causal explanation.
