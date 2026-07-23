# Research Knowledge Organization Model

This model is the skill-owned minimum contract for organizing research knowledge. Repository profiles bind or tighten it without becoming a prerequisite for the skill.

## Layers

1. **Built-in organization** defines node roles, default paths, ownership, lifecycle, relationships, and validation gates.
2. **Repository profile** supplies local policy documents, domain patterns, path overrides, templates, and stricter validation.
3. **Scoped governance** such as `AGENTS.md` supplies human-readable instructions that remain authoritative for work in its scope.

Resolve these layers before creating a promotion plan. Record the built-in schema hash, default-profile hash, repository-profile hash, and policy documents in validation output.

## Stable Semantics

| Node | Responsibility |
|---|---|
| domain entry | Scope, reading path, and complete canonical index. |
| survey | Cross-work taxonomy, comparison, timeline, trend, and synthesis. |
| paper | Complete single-work mechanism, implementation, evidence, and limitations. |
| topic | Stable concept or pipeline shared across works. |
| evidence | Selection, provenance, index, count, inventory, and audit metadata. |
| supplement | Final non-canonical presentation or interactive derivative backed by canonical Markdown. |
| asset | One formally referenced object owned by exactly one Survey or Paper. |
| process artifact | Search, source, PDF, render, crop-in-progress, script, cache, manifest, log, or QA output. |

Default publication relationships are:

```text
domain entry -> survey -> paper -> asset
      |            |        |
      +--------> topic      +-> evidence
      +--------> evidence
```

Repositories may add relationship types or change path bindings, but must preserve canonical ownership, process/formal separation, resolvable links, and auditable evidence.

## Merge Policy

- Allow profiles to override paths, templates, domain patterns, relationship-block style, and validation severity.
- Allow profiles to add document types, relationships, forbidden patterns, and policy documents.
- Do not allow a profile to remove canonical ownership or make process artifacts formal by omission.
- Treat unknown profile fields as validation errors.
- Treat incompatible schema-major versions as errors.

## Discovery

Resolve the repository profile in this order:

1. explicit `--profile`;
2. `RESEARCH_KB_PROFILE` environment variable;
3. nearest `research-knowledge.profile.json` (preferred) or `.research-knowledge.json` (compatibility), searching from the target domain toward repository root;
4. built-in `default-profile.json` only.

Always read applicable scoped governance separately. A repository profile may list additional policy documents, but their absence does not disable the built-in organization.
