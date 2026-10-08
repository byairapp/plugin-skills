---
name: byair-flight-brief
description: Check a flight's current status, delays, gate changes and incoming aircraft using byAir. Use when asked whether a flight is delayed, on time or where its plane is.
---

# byAir flight brief

Requires the connected byAir plugin or MCP connector. Use its available tools and current schemas; names below are logical names and clients may namespace them. If a required tool or connection is unavailable, explain what could not be checked. Use the user's language.

## Resolve the flight

Use an existing flight ID, `byair_list_trips` for tracked flights, or `byair_suggest` and the flight search tools for a flight code/date. For the user's own flights, use `ownership="mine"`; use friend or all only when the request needs that scope. Select `status="active"` or `"expired"` to match the requested date. Follow `next_offset` while `has_more` only when needed to find the flight.

Flight-number parameters contain digits only with a separately resolved airline ID. Match the departure-local date and route, not only the flight number. Ask about the date or candidate only when the request and available context cannot resolve it.

When the selected entry contains `codeshareId`, call `byair_get_flight_by_codeshare(codeshare_id=...)`. Otherwise use `byair_get_flight` or `byair_get_flight_by_number` with the parameters required by its schema. Codeshare detail keeps the marketing code/airline while `id` remains the operating flight ID; retain `operator.codeshareId` when returned.

## Give the brief

Lead with the flight code, route, date and `computed_status` / `computed_status_detail`. Include useful scheduled, estimated or actual times, terminal and gate, keeping the time types distinct. Display airport-local timestamps as returned; convert only when requested. Missing data is unknown, not evidence that the flight is on time. Distinguish upcoming phases from phases already in progress using `computed_phase` and `computed_phase_state`.

For delay or aircraft questions, use returned `inbound` as incoming-aircraft context. Keep predicted delay separate from observed delay. Incoming aircraft position is not the requested flight's position; current aircraft data does not establish historical flight position. Use `byair_get_flight_aircraft` only when additional aircraft details are requested or material to the answer. If the response supplies an update timestamp, include it when freshness matters; do not invent a last-updated time or promise continuous monitoring.

An absent `ownership` does not mean this is the user's flight. A status question does not authorize tracking, Skip, notification changes or messages. If a share link is requested, use `byair_generate_share_details` with the operating `flight_id` and selected `codeshare_id` when applicable; return the link without sending it to anyone.
