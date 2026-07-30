# Contributing

## File conventions

- Use UTF-8 Markdown.
- Use English `kebab-case` file names.
- Keep one primary technical subject per file.
- Include YAML front matter for product and standards records.
- State assumptions and unknowns explicitly.
- Link to sources and related records.
- Never publish client-confidential drawings, prices, personal data, passwords, keys, or licensed standards.

## Review workflow

1. Create or update a record using the relevant template.
2. Mark new content `draft`.
3. Attach or reference supporting controlled documents.
4. Request technical review.
5. Change to `reviewed` or `verified` only after approval.
6. Record material changes in `CHANGELOG.md`.

Run the automated checks before requesting review:

```bash
python scripts/validate_content.py
```

Pull requests should pass the knowledge-base validation workflow and receive
CODEOWNER review. Repository administrators should configure branch protection to
require those checks.

## Writing standard

- Prefer precise engineering language over marketing claims.
- Separate verified facts from recommendations.
- Include units with every numeric value.
- State standard edition/year when known.
- Avoid unqualified words such as “all,” “zero leakage,” “maintenance-free,” or “fully compliant.”

## Evidence and search results

- Use search engines only to discover sources; cite the underlying page or document.
- Distinguish `source-claimed`, `externally-corroborated`, and `verified` evidence.
- A `verified` record requires a named authorized reviewer and controlled evidence.
- Follow the [source quality policy](docs/source-quality-policy.md) and
  [document control policy](docs/document-control-policy.md).
