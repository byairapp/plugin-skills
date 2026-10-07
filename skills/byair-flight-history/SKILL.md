---
name: byair-flight-history
description: Summarize flights recorded in byAir with yearly totals and airline, airport, route or aircraft breakdowns. Use for personal flying statistics or flights within a statistics group.
---

# byAir flight history

Requires the connected byAir plugin or MCP connector. Use its available tools and current schemas; clients may namespace tool names. Explain when the account connection, required tool or requested data is unavailable. Use the user's language.

## Summarize recorded history

Use `byair_get_stats` for headline statistics. Use `byair_get_detailed_stats` for a yearly breakdown or airline, airport, route, country, aircraft, calendar, seat or alliance grouping. The detailed tool takes no parameters: select the requested period from its response rather than inventing a year input.

Answer for the period and category requested. State that the figures describe flights recorded in byAir, using the supplied units and counts. An absent breakdown is unknown rather than zero. Do not infer complete travel history or unsupported metrics such as emissions. Where `count` and `flightsCount` both appear, preserve their supplied meaning rather than assuming they are interchangeable.

## Resolve a group follow-up

Use the group's `singleFlight` directly when available, or pass its opaque `flightsRef` as `ref` to `byair_get_stats_flights`. Resolve only groups needed for the question, not every group. Do not decode or fabricate refs.

On `INVALID_REF`, reread detailed statistics and obtain a fresh ref for the selected group; stop if a fresh lookup still fails. On `REF_USER_MISMATCH`, explain that the reference cannot be used for this account; do not change accounts or retry it.

Compact group flights do not contain full Timeline or inbound data. Fetch flight detail only when the follow-up needs it, using `byair_get_flight_by_codeshare(codeshare_id=...)` when a compact entry has `codeshareId`. Preserve the selected marketing identity and operating flight ID. Do not use a live aircraft position as a historical flight position.

## Export only on request

Inspecting or summarizing history does not authorize an email export. Use `byair_export_flights` only for an explicit export request with a resolved recipient email; clarify the recipient if ambiguous. The tool requests a backend email. A successful response does not prove that the email was delivered.
