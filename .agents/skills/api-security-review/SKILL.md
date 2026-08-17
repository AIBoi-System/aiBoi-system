---
name: api-security-review
description: Reviews AiBoi API endpoints for authentication, authorization, tenant isolation, input validation, sensitive data exposure, OWASP API Security Top 10 risks, and secure backend practices. Use when creating, reviewing, or modifying FastAPI endpoints, authentication flows, uploads, permissions, or operations involving sensitive business data.
---

# API Security Review

## Purpose

This skill defines the mandatory security review process for every API implemented in the AiBoi project.

Its goal is to ensure that every endpoint complies with the project's security standards before being considered complete.

The review covers authentication, authorization, data protection, tenant isolation, validation, secure persistence, logging, and OWASP API Security Top 10 recommendations.

This skill should be applied during:

- implementation of new endpoints;
- code reviews;
- pull request reviews;
- security audits;
- bug fixes involving APIs;
- authentication changes;
- authorization changes.

---

# Context

AiBoi is a livestock management system that stores sensitive information including:

- personal information;
- farm information;
- production history;
- reproductive records;
- sanitary records;
- financial information (future modules);
- subscription information;
- GPS and IoT data (future modules).

Protecting this information is mandatory.

---

# Security Principles

Always follow these principles:

- Least Privilege
- Defense in Depth
- Deny by Default
- Secure by Default
- Fail Securely
- Principle of Least Knowledge
- Never Trust Client Input
- Backend is the Source of Truth

---

# When to use this skill

Use this skill whenever the task involves:

- FastAPI endpoints
- REST APIs
- Authentication
- Authorization
- JWT
- Login
- Logout
- Password recovery
- User registration
- File uploads
- CRUD operations
- Animal APIs
- Property APIs
- Reports
- Dashboard APIs
- Sensitive information
- Administrative endpoints
- External integrations
- Payment endpoints
- Notification endpoints

Keywords:

API

FastAPI

JWT

Security

OWASP

Authentication

Authorization

Permissions

Upload

IDOR

BOLA

Tenant

---

# When NOT to use this skill

Do not activate this skill for:

- Flutter UI changes
- Pure documentation
- Figma screens
- Business rule modeling without APIs
- SQL performance optimization only
- Visual refactoring

Use more appropriate skills instead.

---

# Required Context

Before reviewing an endpoint, locate and read:

## Documentation

- docs/05-security/
- docs/07-api/
- docs/13-modules/<module>/
- docs/02-mvp/

## Backend

- authentication implementation
- authorization implementation
- router
- use case
- repository
- tests

Never assume file paths.

Always inspect the current project structure first.

---

# Review Workflow

Execute the following checklist in order.

---

# Step 1 — Endpoint Identification

Identify:

- HTTP Method
- URL
- Module
- Request Model
- Response Model
- Use Case
- Repository
- Database Tables
- External Integrations

---

# Step 2 — Authentication

Verify:

✓ Endpoint requires authentication when appropriate

✓ Token is validated

✓ Expired tokens are rejected

✓ Invalid tokens return Unauthorized

✓ Disabled users cannot authenticate

✓ Public endpoints are explicitly documented

Never trust tokens coming from the frontend without validation.

---

# Step 3 — Authorization

Verify:

- user permissions
- ownership
- resource permissions
- administrator permissions

Authorization MUST happen on the backend.

Hiding buttons in Flutter is NOT authorization.

---

# Step 4 — Tenant Isolation

AiBoi is multi-property.

Every protected resource must belong to the active property.

Never query resources only by ID.

❌ Wrong

```python
animal = repository.get(animal_id)
```

✔ Correct

```python
animal = repository.get(
    animal_id=animal_id,
    property_id=current_property.id,
)
```

Verify:

- owner
- property
- employee access
- shared resources
- property filters

Attempt cross-property access.

It must fail.

---

# Step 5 — OWASP API Security Top 10

Review every endpoint against:

API1

Broken Object Level Authorization

API2

Broken Authentication

API3

Broken Object Property Level Authorization

API4

Unrestricted Resource Consumption

API5

Broken Function Level Authorization

API6

Unrestricted Access to Sensitive Business Flows

API7

Server Side Request Forgery

API8

Security Misconfiguration

API9

Improper Inventory Management

API10

Unsafe Consumption of APIs

---

# Step 6 — Input Validation

Validate:

- required fields
- enums
- strings
- dates
- UUIDs
- IDs
- file types
- MIME types
- numeric ranges
- maximum length
- minimum length

Never trust frontend validation.

---

# Step 7 — Sensitive Data

Never expose:

- password hash
- password
- JWT
- Refresh Token
- CPF
- internal IDs
- SQL errors
- stack traces
- internal exceptions

Return only what the client actually needs.

---

# Step 8 — Database Access

Verify:

- parameterized queries
- ORM usage
- transaction boundaries
- rollback
- soft delete
- optimistic updates
- duplicate writes

Never concatenate SQL strings.

---

# Step 9 — Logging

Never log:

- passwords
- tokens
- refresh tokens
- card numbers
- CVV
- CPF
- secrets
- API Keys

Logs must be useful without exposing sensitive information.

---

# Step 10 — File Uploads

Verify:

- allowed extensions
- MIME validation
- maximum size
- generated filenames
- authorization
- antivirus strategy (future)
- path traversal protection

Never trust filenames sent by clients.

---

# Step 11 — HTTP Security

Review:

- HTTPS
- CORS
- Security Headers
- Cache headers
- Cookies
- SameSite
- Secure
- HttpOnly

---

# Step 12 — Rate Limiting

Critical endpoints should support protection against abuse.

Especially:

- login
- password reset
- registration
- uploads
- search
- reports

If rate limiting is missing:

Document the risk.

Do not introduce new dependencies without approval.

---

# Step 13 — Error Handling

Verify:

- generic messages
- correct HTTP status
- no stack trace
- no internal information leakage

Example:

✔

"Invalid credentials."

❌

"Password does not match hash."

---

# Step 14 — Destructive Operations

Review:

DELETE

PATCH

PUT

Deactivate

Cancel

Archive

Verify:

- authorization
- audit
- soft delete
- rollback
- business rules

---

# Decision Tree

## Public endpoint?

Yes

↓

Validate inputs

↓

Rate limit if necessary

↓

Review exposed data

No

↓

Authentication required

↓

Authorization required

↓

Tenant isolation required

---

## Property Resource?

Yes

↓

Validate property ownership

↓

Filter by property_id

↓

Test cross-property access

No

↓

Continue normal review

---

## Changes data?

Yes

↓

Transaction

↓

Rollback

↓

Audit

↓

Permissions

No

↓

Review response only

---

# AiBoi Conventions

Always

- Validate JWT
- Validate ownership
- Validate property
- Validate permissions
- Use repositories
- Use use cases
- Keep business rules outside routers

Never

- Query sensitive resources by ID only
- Trust Flutter
- Store passwords
- Store secrets
- Return stack traces
- Disable authorization to "make tests pass"

---

# Review Output

Always produce:

## Critical Issues

...

## High Issues

...

## Medium Issues

...

## Low Issues

...

## Recommendations

...

## Missing Tests

...

## Security Score

0–100

Explain the score.

---

# Self Verification

Before finishing confirm:

- [ ] Authentication reviewed
- [ ] Authorization reviewed
- [ ] Tenant isolation verified
- [ ] IDOR tested
- [ ] OWASP API Top 10 reviewed
- [ ] Sensitive fields protected
- [ ] Validation complete
- [ ] Database access reviewed
- [ ] Transactions reviewed
- [ ] Logging reviewed
- [ ] Uploads reviewed
- [ ] Rate limiting considered
- [ ] Error handling reviewed
- [ ] Documentation updated if necessary
- [ ] No security regression introduced

---

# References

- OWASP API Security Top 10
- OWASP ASVS
- OWASP Cheat Sheets
- FastAPI Security Documentation
- PostgreSQL Security Best Practices
- Clean Architecture
- Domain-Driven Design (DDD)
- AiBoi Security Documentation