# Deployment Compliance — the pre-non-synthetic wall

**Reader:** the person deciding whether an OSSICRO deployment may ever hold a
**real** (non-synthetic) case, and any reviewer auditing that decision.
**Governed by:** `docs/OSSICRO-CONSTITUTION.md` (drafts only; no PHI egress;
HC1–HC7) and Overhaul Package 9 (M9, m14, m15, m17, m18, m20).
**This document states requirements. It does not certify that any deployment
meets them — that certification is a qualified human's act, reviewed before
any real-PHI decision (a standing gate; nothing in code waives it).**

## 1. Scope of the shipped pilot (M9)

The shipped configuration is a **single-user, single-machine, loopback-only
pilot over synthetic cases**. Concretely:

- The server binds `127.0.0.1:8765` and **refuses to start on any
  non-loopback host** (`app/server.py:_bind_refusal`, the M9a bind guard).
  Overriding requires **both** `OSSICRO_ALLOW_NONLOCAL_BIND=1` **and** a
  configured authentication backend — and no authentication backend exists in
  this build (`_auth_backend_configured()` is hard-coded `False`), so the
  override **cannot currently succeed**. This is deliberate: the standing
  no-bind-change rule is program-enforced, not a convention.
- There is **no persona authentication** (INV-7). A case id is a full-access
  capability on `GET /api/case/{id}`. That is acceptable only while the sole
  user is the requesting physician on their own machine — hence the guard.
- The physician UI footer states the same boundary to the user:
  *"Single-user local pilot — do not expose this server or share case URLs."*

## 2. The covered-entity boundary (M9b)

OSSICRO the software is not a covered entity. The **deploying physician or
practice almost certainly is** (a HIPAA covered entity or part of one), and a
hosted deployment operator would be a **business associate**. The moment a
real patient's case enters the store, everything downstream of intake is that
covered entity's PHI processing, and:

- the machine running OSSICRO is inside the covered entity's compliance
  boundary (device inventory, access control, audit obligations);
- any party hosting, backing up, or administering that machine for the
  physician needs a **business associate agreement (BAA)**;
- the HIPAA disclosure-basis mechanics OSSICRO records (preparatory review →
  the promote act's recorded `legal_basis`) describe the covered entity's own
  obligations — recording them in OSSICRO does not discharge them.

## 3. The case store is PHI the moment a real case exists (M9c)

`app/data/cases/{id}.json` stores intake **values in the clear** (that is the
design — the input-of-record must be reviewable). With synthetic fixtures this
is inert. With one real patient it is PHI at rest, immediately, and:

- **Encryption at rest is expected** — full-disk encryption at minimum;
  the app itself does not encrypt the store and does not claim to.
- The committed-profile object stores **hashes, never values** (INV-8), and
  as of m14 those hashes are **HMAC-SHA256 keyed** under a server-side secret
  (`app/data/secret.key`, created on first run, mode 0600, gitignored, never
  written into a case JSON). An unkeyed hash of a low-entropy value is
  recoverable by enumeration; the keyed scheme closes that. Old unkeyed
  commits fail **loud** (every field reads pending; a named recommit is the
  repair) — never silently wrong.
- The audit trail is append-only and value-free by construction, but it is
  still part of the record set: it travels with the case under the same
  protections.
- The patient-view token is a bearer capability: it is masked in the request
  log (m17) and compared in constant time, but anyone holding it can read the
  plain-language status page. Treat minted links accordingly.

## 4. BAA inventory (M9d)

Before any real case, enumerate every party that could touch case content:

| Party | When it touches PHI | Requirement |
|---|---|---|
| Model API provider (Anthropic) | Only if `OSSICRO_LIVE_CONCEPT_REVIEW` is affirmatively enabled — rendered document text egresses | BAA **or** documented de-identified projection, zero retention, named enabler on record — see [`AI-REVIEW-PRECONDITIONS.md`](AI-REVIEW-PRECONDITIONS.md) |
| Host / infrastructure operator | If the machine, its backups, or its disks are managed by anyone other than the covered entity | BAA before the first real case |
| External registries (clinicaltrials.gov etc.) | Never receives PHI by construction (INV-4 closed predicates; live egress disabled pending greenlight) | No BAA; the residual inference-egress risks are documented in `engine/ossicro/egress.py` |
| Backup / sync tooling | Any copy of `app/data/` | Same standing as the store itself: encrypted, BAA'd if third-party |

The shipped default egresses nothing: the concept reviewer is the offline
stub and registry matching runs against the local mock adapter. Every switch
away from a default is a named human act with its own preconditions.

## 5. Retention and deletion (M9e)

- The store keeps a case until a human deletes its JSON file; OSSICRO never
  deletes on its own (an automated deletion would be an un-audited act).
- The audit trail is append-only **inside** a case. Deleting the case file
  deletes its trail — retention of the record set is the covered entity's
  duty under its own medical-records and Part-11-adjacent obligations, not
  something the software can decide. Establish a retention schedule before
  the first real case; investigational-record retention runs at least two
  years past the dates in 21 CFR 312.57(c)/312.62(c) for a sponsor-
  investigator. *(PENDING-HUMAN-VERIFICATION: confirm the exact retention
  trigger dates in 312.57(c)/312.62(c) against eCFR before relying on this
  schedule — stated here to the best-known target, not silently asserted as
  final.)*
- `app/data/secret.key` must be retained as long as any committed profile it
  keyed is retained (losing it makes every profile re-verify as pending —
  loud, recoverable by recommit, but avoidable).
- Backups inherit the schedule: a deleted case that lives on in a backup is
  not deleted.

## 6. Preconditions for any non-synthetic pilot — not deferrals

These two items are frequently mislabeled "deferred." They are
**preconditions**: the wall this document exists to state.

1. **INV-7 persona authentication.** Every persona surface (physician,
   manufacturer inbox, CRO board) is unauthenticated today. No real case may
   enter a deployment until a named-human authentication backend exists and
   `_auth_backend_configured()` truthfully reports it. The bind guard makes
   this structural: without it the server cannot even be exposed.
2. **m14 keyed profile hashes.** Shipped and always-on in the app (the
   server keys every hash under `app/data/secret.key`). A deployment that
   bypassed the app layer and wrote unkeyed profiles would reopen the
   enumeration hole — do not.

Also standing, from their own documents: the live concept reviewer's
preconditions ([`AI-REVIEW-PRECONDITIONS.md`](AI-REVIEW-PRECONDITIONS.md)),
and the INV-4 live-egress greenlight (off; flipping it is an explicit human
act recorded in code review, never configuration).

## 7. What turning any of this off would mean

There is no supported configuration that weakens the above. The bind guard,
the keyed hashes, the audit records on export/release/promote, and the
escalate-only identifier lint (m20 — it warns on identifier-shaped text in
free-text fields at release and egress time; it never blocks and never
rewrites) are all part of the pre-non-synthetic wall. A fork that removes
them is a different product with a different risk posture, and the person
who forks it owns that posture.
