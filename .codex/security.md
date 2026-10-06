# Security Rules

## Secrets and data

Never commit, log, return, or hardcode:

- `.env` files or environment-specific credentials
- API keys, tokens, passwords, private keys, or database secrets
- personal data beyond what the assigned task strictly needs

Use environment variables or the existing configuration approach for sensitive runtime values. Ensure new secret-file patterns are ignored by Git. Do not remove license or attribution files without explicit instruction.

## Inputs and errors

- Treat browser input, HTTP payloads, CSV files, environment values, and model input as untrusted.
- Validate type, format, range, size, and required fields at the boundary appropriate to the input.
- Never trust client-provided values blindly.
- Do not introduce `eval`, shell execution of untrusted input, unsafe deserialization, or path traversal behavior.
- Do not weaken authentication, authorization, CORS, validation, or error handling to make an implementation or test pass.
- Return minimal client-safe error information and keep operational details in controlled server logging only.

## Dependencies

- Add a dependency only when the current task needs it and the standard library or existing dependencies cannot solve the problem clearly.
- Review its maintenance, security posture, license compatibility, and integration cost before adding it.
- Keep version and installation changes scoped to the relevant manifest(s); do not casually update unrelated dependencies.
