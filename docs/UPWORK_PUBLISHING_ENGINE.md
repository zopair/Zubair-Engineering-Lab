# Upwork Publishing Engine — Research and Implementation Plan

**Status:** Approved capability candidate; implementation not started  
**Updated:** 2026-11-11  
**Owner:** Zubair Engineering Lab  
**Primary objective:** Prepare and publish accurate Freelancer Portfolio projects and Project Catalog services through the user's authenticated Upwork session, with human approval at the final publication boundary.

## 1. Decision

Build a lab-owned publishing workflow using a browser automation adapter. Prefer **Playwright** as the underlying browser automation interface and evaluate **Playwriter** as the first interactive/session bridge. Keep **Browser Use** as an alternative agentic browser adapter if deterministic Playwright flows prove insufficient.

Do not depend on undocumented Upwork write APIs or reverse-engineered private GraphQL mutations. Use the normal Upwork user interface, subject to Upwork's terms, security controls, and supported interaction patterns.

This is a capability for preparing and assisting publication, not an autonomous proposal sender. It must never spend Connects, submit proposals, change account identity/payment settings, or publish a listing without explicit user approval for that action.

## 2. Research inventory

### Preferred browser foundations

| Project | Repository | Intended use | Decision |
|---|---|---|---|
| Playwriter | https://github.com/nshkrdotcom/playwriter | Connect automation to an already authenticated browser session; useful for interactive, user-visible control | First candidate to inspect and evaluate |
| Browser Use | https://github.com/browser-use/browser-use | Agentic browser navigation and interaction when page structure changes or a multi-step workflow needs semantic control | Secondary candidate; compare after Playwriter evaluation |
| Playwright | https://github.com/microsoft/playwright | Deterministic browser automation, locators, screenshots, traces and repeatable UI tests | Core automation interface / fallback |

### Upwork-specific research references

These are research references, not approved production dependencies and not evidence of Portfolio or Catalog publishing support.

| Project | Repository | Potential value | Limitation / handling |
|---|---|---|---|
| Upwork MCP | https://github.com/vanooo/upwork-mcp | Reference for Upwork-oriented MCP tool design and read/workflow integration | Audit implementation, license, maintenance and actual supported actions before reuse; do not assume it can publish Portfolio or Catalog |
| Upwork Autopilot | https://github.com/klajdikkolaj/upwork-autopilot | Reference for job discovery and workflow automation patterns | Not a publishing engine; do not enable proposal submission or Connect spending |
| Official Upwork Node SDK | https://github.com/upwork/node-upwork | Historical reference for OAuth/API integration concepts | Repository is archived; not a current supported publishing path |

### Research conclusions

- No reviewed repository has been established as a ready-made, reliable publisher for Freelancer Portfolio projects or Project Catalog services.
- Browser automation is the practical route to investigate because it can operate the same user-facing forms available to the account.
- The existence of a browser automation framework does not establish that Upwork permits every automated interaction. Check current platform terms and respect CAPTCHA, MFA, rate limits, bot checks and any explicit prohibition. Do not evade controls.
- The official API/read capabilities and third-party Upwork MCP projects may be useful for discovery or account context, but are not treated as write authorization for Portfolio or Catalog.

## 3. Target architecture

```text
Engineering Lab Registry / Portfolio Sources
                 |
                 v
       Publishing Content Adapter
                 |
                 v
      Validation & Policy Gate
                 |
                 v
      Browser Session Adapter
       (Playwright / Playwriter)
                 |
                 v
       Upwork User-facing UI
                 |
                 v
      Human Review and Approval
                 |
                 v
        Publish / Save Draft
                 |
                 v
       Post-publication Verification
```

### Components

1. **Content source adapter**
   - Reads approved project metadata from the lab registry and portfolio directory.
   - Reads project title, role, description, skills, deliverables, images, URLs and service package definitions.
   - Preserves source provenance and version/commit reference.

2. **Content validator**
   - Checks required fields, character limits, skill limits, package consistency, price/delivery/revision values and link validity.
   - Rejects unsupported claims and content that is not traceable to project artifacts.
   - Keeps the user's neutral presentation rule: describe capabilities and deliverables; do not add unnecessary defensive statements or imply unperformed work.

3. **Browser session adapter**
   - Uses a user-authenticated browser session.
   - Does not request or store the user's Upwork password, session cookies or MFA codes in repository files.
   - Supports visible operation, screenshots and step-level logs with sensitive values redacted.
   - Stops when login, MFA, CAPTCHA, bot verification or an unexpected security prompt is required.

4. **Workflow modules**
   - Freelancer Portfolio: create/edit project, upload permitted media, save and verify.
   - Project Catalog: configure service, tier/package data, requirements, FAQs, gallery media and review submission.
   - Draft/review state must be distinguished from published/approved state.

5. **Approval gate**
   - Show the exact final values and media before any irreversible submission.
   - Require explicit approval for each publish/submit action.
   - Saving a draft may be automated only when the user has authorized that specific workflow.

6. **Verification**
   - Re-open the relevant profile/catalog page after submission.
   - Confirm the listing appears and capture its canonical URL and visible status.
   - Record platform review status separately from publication status.
   - Never report success based only on a button click or a submitted form.

## 4. Security and compliance boundaries

- No private API reverse engineering, undocumented mutation calls, CAPTCHA solving, MFA bypass, fingerprint spoofing, proxy rotation or bot-detection evasion.
- No credential, cookie, token, personal data or client information committed to Git.
- Use a local secret store or environment injection only where genuinely required; prefer the browser's existing authenticated session.
- Redact email addresses, account identifiers, cookies, tokens and private client information from traces/screenshots.
- Respect Upwork rate limits, terms, and any platform restrictions on automated access.
- No proposal submission, Connect spending, contract acceptance, payment action, account setting change or client messaging in this capability.
- User approval is mandatory immediately before every public publish/submit action.

## 5. Implementation phases and acceptance criteria

### UPW-PUB-001 — Source and license audit
- Inspect current README, release activity, dependencies and license for Playwriter, Browser Use and Playwright.
- Inspect the Upwork-specific reference repositories only for reusable patterns.
- Record exact commit/tag, license, maintenance signals and security concerns.
- Acceptance: comparison table and dependency decision record committed.

### UPW-PUB-002 — UI workflow reconnaissance
- Manually map current Upwork Freelancer Portfolio and Project Catalog flows.
- Record field labels, required fields, validation messages, image constraints and save/publish states.
- Acceptance: versioned UI workflow specification with screenshots sanitized of personal data.

### UPW-PUB-003 — Content schema and validator
- Define versioned YAML/JSON schemas for Portfolio projects and Catalog services.
- Add field-length, package arithmetic, skill-count, URL and evidence/provenance validation.
- Acceptance: unit tests for valid content, missing fields, boundary lengths, invalid pricing and unsupported claims.

### UPW-PUB-004 — Browser adapter proof
- Start with a visible, user-authenticated browser session.
- Implement navigation and form inspection without submitting public changes.
- Acceptance: repeatable navigation, screenshot/trace evidence, safe stop on login/MFA/CAPTCHA, no credential persistence.

### UPW-PUB-005 — Draft population
- Populate one user-selected Portfolio item or Catalog service as a draft, stopping before final publication.
- Acceptance: field-by-field comparison against the approved source payload and user review.

### UPW-PUB-006 — Approved publication and verification
- Publish only after the user reviews the exact final content and explicitly approves.
- Verify the resulting public/profile state and record the canonical URL.
- Acceptance: independently re-opened listing with matching title/content and visible status.

### UPW-PUB-007 — Batch support
- Add queueing, resumability, idempotency checks and per-item approval.
- Acceptance: reruns do not create duplicate listings; partial failures are recoverable and reported.

## 6. Initial content targets

The first intended service categories are:

1. Responsive Landing Page Development & Fixes
2. Python, Excel & Data Automation
3. REST API Integration & Testing

The Freelancer Portfolio should draw from the eight existing engineering portfolio projects. Do not duplicate the Agency Portfolio into the Freelancer Portfolio without checking each item's title, media and account-specific requirements.

## 7. Non-goals

- Automatically applying to jobs or sending proposals.
- Spending Connects or optimizing proposal volume.
- Scraping private client data.
- Circumventing Upwork security controls or platform review.
- Claiming that a listing is published, approved or live without post-submission verification.
- Cloning all candidate repositories into the lab before a dependency is selected.

## 8. Immediate next action

Start with **UPW-PUB-001**: audit Playwriter, Browser Use and Playwright source/license/maintenance, then select one browser adapter. In parallel, manually document the current Portfolio and Catalog forms. No additional infrastructure is required before this work begins.
