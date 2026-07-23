# Knowledge Base Publication Contract

## 1. Authority

The skill-owned organization model supplies the portable minimum contract. Resolve it with an optional repository profile, then read applicable scoped governance and profile-listed policy documents. Repository policy may bind paths and tighten rules without being required for the skill to operate.

## 2. Object Model

Every promoted object has:

| Field | Meaning |
|---|---|
| `canonical_id` | Stable identity across versions and sources. |
| `domain` | Owning knowledge domain. |
| `doc_type` | `survey`, `paper`, `topic`, `evidence`, or `supplement`. |
| `slug` | Stable kebab-case path name. |
| `canonical_path` | One authoritative formal path. |
| `owner` | Survey or Paper that owns an asset or conclusion. |
| `operation` | `create`, `update`, `link-only`, or `no-promotion`. |

Use `link-only` when another domain already owns the entity. Never create a local shadow copy to simplify links.

## 3. Relationship Types

Use ordinary Markdown links to encode:

- `surveys`: Survey summarizes a Paper or method family.
- `implements`: repository or system implements a method.
- `adopts`: model system uses a technology.
- `uses-kernel`: model or method uses a runtime/kernel.
- `extends`: a work directly extends another.
- `compares`: a work evaluates against another.
- `evidence-for`: Evidence supports a Survey/Paper claim.
- `background-for`: Topic provides stable background.

Relations do not change canonical ownership.

## 4. Promotion Decisions

Promote only stable, reusable knowledge:

- Promote a Paper when it has enough evidence to support a standalone mechanism/result record.
- Promote a Topic when the concept spans papers and is not an experiment from one paper.
- Promote Evidence when provenance, selection, counts, or inventories must remain auditable.
- Keep raw search results, PDFs, source trees, page renders, extraction attempts, scripts, logs, and manifests under the resolved process root.

## 5. Cross-Domain Example

For a video model with a native sparse-attention component:

- the full model report may be owned by a model-systems domain;
- sparse-attention adoption evidence may be owned by an infrastructure domain;
- the sparse-attention Survey links to the canonical model Paper and adoption Evidence;
- original model figures stay with the model Paper owner;
- no duplicate Paper or asset is created under custom attention.

## 6. Publication Gates

Before declaring promotion complete, verify:

1. Domain, document type, slug, owner, and operation are explicit.
2. Existing canonical nodes were searched and reconciled.
3. Formal content and assets are in owner-specific locations.
4. README indexes every new canonical document.
5. Survey-to-Paper/Evidence and Paper-to-README/Survey links exist.
6. Figure inventory records caption, page, crop, usage, and original-resolution QA.
7. Formal references are relative, resolvable, and Git tracked.
8. No formal document references the resolved process root, local absolute paths, page renders, or temporary files.
9. Orphan documents and assets are resolved or explicitly blocked.
10. Git changes remain isolated by domain; do not commit unless requested.
