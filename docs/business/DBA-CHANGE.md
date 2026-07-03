# DBA Change: desertskyaz.com → Desert Sky Development

**Status:** Planning / not yet filed
**Last updated:** 2026-07-03

## Summary

The business currently operates as a single-member Arizona LLC, doing
business under the formally registered Arizona trade name
`desertskyaz.com`. We are renaming the trade name (DBA) to
**Desert Sky Development**, to align the brand with the software
development work the business actually does. The LLC's own legal name
(as filed with the Arizona Corporation Commission) is **not** changing —
only the trade name/DBA.

This distinction matters because it substantially shrinks the federal
side of the work: a DBA-only change does not require notifying the IRS
or getting a new EIN. If we ever decide to also rename the LLC entity
itself (not just the trade name), that is a separate, larger process —
see "If you also want to rename the LLC itself" below.

## What changes, legally

| Level | What's on file | Changing? |
|---|---|---|
| Arizona Corporation Commission | LLC's legal/registered name, statutory agent, articles of organization | **No** |
| Arizona Secretary of State | Trade Name / Trademark registration (`desertskyaz.com`) | **Yes** — new trade name filing |
| Arizona Dept. of Revenue (AZTaxes.gov) | TPT license DBA field (if a TPT license is on file) | **Yes**, if applicable |
| IRS (EIN record) | Legal business name tied to EIN | **No** — DBA-only changes don't require IRS notice |
| Everything else (bank, contracts, site, invoices, etc.) | Brand-facing use of the name | **Yes** — operational cleanup |

## Arizona trade name filing (the core state action)

- Filed with the **Arizona Secretary of State**, Trade Name & Trademark
  (TNTM) division — not the Corporation Commission.
- Arizona has no formal "amend a trade name" filing for a name change —
  in practice you register the new trade name (`Desert Sky Development`)
  as a new application, and let the old one (`desertskyaz.com`) lapse or
  cancel it. Confirm current mechanics on the portal before filing, since
  a same-owner rename can occasionally be routed as an amendment attached
  to a renewal.
- Cost: **$10** online filing (+ optional $25 expedite). Processing is
  ~3-4 weeks standard, faster with expedite. Filed at
  [azsos.gov/business/tntm](https://azsos.gov/business/tntm).
- Trade names run 5 years from grant date and must be renewed ($10) or
  they lapse.
- Before filing, search the AZ SOS trade name/trademark database and do
  a basic USPTO TESS search for "Desert Sky Development" (and close
  variants) to avoid stepping on an existing mark — not required, but
  cheap insurance before printing it on everything.

## Arizona Dept. of Revenue — Transaction Privilege Tax (TPT) license

If the LLC holds an active TPT license (Arizona's version of a sales tax
license — relevant if any part of the work is taxable, e.g. packaged
software/SaaS licensing rather than pure custom dev services), the DBA on
that license needs to be updated separately, via AZTaxes.gov → Account
Update. Fee is **$12 per location** (state) plus any city fee. The
license number itself does not change, but a corrected license is
reissued. If there's no TPT license on file (common for a services-only
dev shop), this step doesn't apply — confirm which situation applies.

## Federal (IRS)

Because only the DBA is changing and the LLC's legal name on file with
the IRS/EIN stays the same, **no IRS notification or new EIN is
required**. The LLC continues filing under its legal name; "Desert Sky
Development" is simply the trade name it does business as. The one place
this does surface federally: on **Form W-9** given to clients, Line 1
must stay the LLC's legal name, with "Desert Sky Development" on Line 2
(business/DBA name) — worth double-checking any W-9 already on file with
existing clients gets reissued with the new DBA on Line 2.

## If you also want to rename the LLC itself (not just the DBA)

Not part of the current plan, but flagging for completeness: that would
require filing **Articles of Amendment** with the Arizona Corporation
Commission (fee + processing time), then updating the IRS record via a
signed letter (or the name-change checkbox on the next return, structure
permitting) referencing the approved amendment, then a full cascade
through bank, contracts, licenses, etc. Meaningfully more work than a DBA
change — only pursue if the LLC's legal name should match the brand
exactly.

## What I (Claude) can't do

I can't file anything with the Arizona Secretary of State, AZ Dept. of
Revenue, IRS, your bank, or any other third party — those all require
your login, signature, and/or payment method. What I can do: research the
requirements (above), draft the checklist, prep any copy/document text
you need to paste into those portals, and update the repo's own
docs/branding references once you confirm the name is filed.

## Sources

- [Arizona SOS — Trade Name & Trademark (TNTM)](https://azsos.gov/business/tntm)
- [AZ SOS Trade Name/Trademark Handbook (PDF)](https://azsos.gov/sites/default/files/docs/bsd_TRADE_NAME-TRADEMARK_handbook_v6_05312024.pdf)
- [Tradename Registration Guidelines — AZ SOS](https://apps.azsos.gov/Business_Services/tnt_name_availability_instructions.htm)
- [Arizona DOR — Updating a TPT Account](https://azdor.gov/business/transaction-privilege-tax/tpt-license/updating-tpt-account)
- [IRS — Business name change](https://www.irs.gov/businesses/business-name-change)
- [LLC University — How to change your LLC name with the IRS](https://www.llcuniversity.com/irs/llc-name-change/)
