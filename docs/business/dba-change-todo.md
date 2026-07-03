# To-Do: Rebrand DBA to "Desert Sky Development"

Reference: see `DBA-CHANGE.md` in this folder for the full research/reasoning
behind each item. This is the action checklist.

Assumptions baked into this list (confirm before relying on it): single-member
Arizona LLC; `desertskyaz.com` is currently a registered AZ trade name; only the
trade name is changing, not the LLC's legal name. Flag me if any of that is
wrong and the list needs to change.

## Phase 0 — Before filing anything

- [ ] Search the [AZ SOS trade name/trademark database](https://azsos.gov/business/tntm) for "Desert Sky Development" and close variants — confirm it's available.
- [ ] Quick search on [USPTO TESS](https://tmsearch.uspto.gov) for the same name, just to avoid an existing federal trademark conflict (not required, but cheap to check now vs. after printing business cards).
- [ ] Decide the exact legal spelling/capitalization you want on file: "Desert Sky Development" vs "Desert Sky Development LLC" vs a d/b/a stylization — pick one and use it everywhere below.

## Phase 1 — State of Arizona filings

- [ ] File the new trade name "Desert Sky Development" with the Arizona Secretary of State at [azsos.gov/business/tntm](https://azsos.gov/business/tntm). Cost: $10 (+$25 optional expedite).
- [ ] Once approved, let the old `desertskyaz.com` trade name lapse, or file to cancel it — don't cancel it before the new one is approved, to avoid a gap with no registered trade name.
- [ ] If the LLC has an active Arizona TPT (sales tax) license: log into [AZTaxes.gov](https://aztaxes.gov) → Account Update, change the DBA field. Cost: $12/location + any city fee. Skip this if there's no TPT license on file.
- [ ] If the business holds any city-level business license (varies by city — Phoenix, Scottsdale, Tempe, etc. each handle this differently), check that city's portal for a name-update requirement. *(Tell me which city and I can pull the specific process.)*

## Phase 2 — Federal

- [ ] Nothing to file with the IRS — confirmed a DBA-only change doesn't require a new EIN or IRS notice, since the LLC's legal name isn't changing.
- [ ] Reissue **Form W-9** to any client/platform that has one on file: Line 1 = LLC's legal name (unchanged), Line 2 = "Desert Sky Development."
- [ ] If the business is registered in **SAM.gov** for any federal contract work, update the DBA/"doing business as" field there too. *(Skip if not applicable.)*

## Phase 3 — Banking & money

- [ ] Bring the approved AZ trade name certificate to the bank to update the DBA on the business checking/savings account.
- [ ] Update the business name/DBA in Stripe, PayPal, Square, or any other payment processor's account settings.
- [ ] Update the business name in accounting software (QuickBooks, Wave, etc.) — check both the "legal name" and "DBA/display name" fields so invoices show the new brand but tax filings still reference the LLC's legal name.
- [ ] Update the name on record with any business insurance policy (E&O / general liability), if one exists.

## Phase 4 — Contracts & clients

- [ ] Draft and send a client/vendor notification (template below).
- [ ] For any active contracts that reference "desertskyaz.com" by name, decide whether a formal amendment/addendum is warranted, or a simple notice is enough (usually fine for a DBA change with no change in the underlying legal entity — check anything with a "no assignment without consent" style clause more carefully).
- [ ] Update invoice/proposal templates to show the new name.

## Phase 5 — Web & digital presence

- [ ] Update website copy, header/footer, and `<title>`/meta tags from desertskyaz.com branding to "Desert Sky Development" (site itself can likely stay on the `desertskyaz.com` domain — the domain doesn't have to match the trade name).
- [ ] Update Google Business Profile name.
- [ ] Update LinkedIn, GitHub org/profile, and any other social/dev-facing profiles (Twitter/X, portfolio sites).
- [ ] Update email signature(s).
- [ ] Update this repo and any other project repos: README, package.json/pyproject "author" fields, LICENSE copyright lines, etc. that currently reference the old DBA.

## Phase 6 — Physical / misc

- [ ] Business cards, letterhead, any signage.
- [ ] Update the "doing business as" name with any professional associations or directories the business is listed in.

---

## Copy-paste: client/vendor notification email

> Subject: Business name update — desertskyaz.com is now Desert Sky Development
>
> Hi [Name],
>
> Quick note: I've updated my business's DBA (trade name) from
> "desertskyaz.com" to **Desert Sky Development**, effective [date]. This
> better reflects the software development work we do together — nothing
> else is changing: same LLC, same EIN, same point of contact, same
> ongoing work.
>
> You'll start seeing "Desert Sky Development" on invoices, contracts, and
> any new paperwork going forward. Let me know if you need an updated W-9
> or anything else on file for your records.
>
> Thanks,
> [Your name]

## Copy-paste: short brand-update blurb (website / social)

> desertskyaz.com is now **Desert Sky Development** — same team, same
> work, a name that actually says what we do: software development.

## Copy-paste: W-9 note

> Line 1 (legal name): [LLC legal name — unchanged]
> Line 2 (DBA/business name): Desert Sky Development
