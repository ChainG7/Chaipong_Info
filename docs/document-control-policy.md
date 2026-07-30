# Document control policy

## Status model

- `draft` — incomplete, unapproved, or based only on public claims.
- `reviewed` — technically reviewed for clarity and source traceability; not
  necessarily approved for design, manufacturing, quotation, or contract use.
- `verified` — checked by an authorized reviewer against identified controlled
  evidence for a stated scope and revision.
- `archived` — retained for history and not current.

## Required metadata

Product records require `document_id`, `title`, `category`, `status`,
`evidence_level`, `owner`, `technical_reviewer`, `last_reviewed`, `source_url`, and
`source_accessed`.

## Verification gate

A record may be changed to `verified` only when:

1. The controlled evidence and applicable revision are identified.
2. The scope of verification is explicit.
3. An authorized technical reviewer is named.
4. Conflicts and open assumptions are resolved or bounded.
5. The pull request records the review decision.

## Review cadence

Review a record when its source changes, a relevant standard or certificate changes,
a product revision is released, a field issue exposes an error, or the document
owner determines that the content may be stale.

## Repository protection

Changes should use pull requests, pass automated content validation, and receive
CODEOWNER review. Branch protection and required reviews must be configured in
GitHub repository settings by an administrator.
