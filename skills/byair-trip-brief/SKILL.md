---
name: byair-trip-brief
description: Brief an upcoming byAir trip with flight legs, current changes, connection timing and airport advice. Use when asked to review a trip, check a layover or prepare for a journey.
---

# byAir trip brief

Requires the connected byAir plugin or MCP connector. Use its available tools and current schemas; clients may namespace tool names. If byAir or a required tool is unavailable, explain which information could not be checked. Use the user's language.

## Find the trip

Use `byair_list_trips(status="active")` with dates or destinations from the request. For the user's own journey use `ownership="mine"`; use friend or all only when the request needs that scope. The default page contains at most 20 whole trips. Follow `next_offset` only when `has_more` and the requested trip or scope needs another page. An absent trip on the first page does not establish that it does not exist. Ask the user to choose when multiple trips match.

Fetch details for relevant legs with `byair_get_flight`, or `byair_get_flight_by_codeshare(codeshare_id=...)` when a leg has `codeshareId`. Keep the selected marketing identity and operating flight ID distinct. Trip-list entries do not contain full Timeline or inbound context. Avoid reading unrelated trips and history.

## Give the brief

Present the itinerary in order with airport-local times, available terminal/gate information and the most relevant current changes. Use `computed_status` and `computed_status_detail` rather than raw status codes. Label scheduled, estimated and actual times separately. Include returned update timestamps when freshness matters; do not invent them.

For connections, compare offset-aware arrival and departure timestamps as instants. Show the interval and identify which time types it uses. Do not subtract airport-local clock labels directly; if dates or offsets are missing, explain that the interval cannot be calculated reliably. Flag different connection airports when shown by the itinerary.

An interval alone cannot establish that a connection is safe. Explain material unknowns such as minimum connection time, baggage recheck, border formalities or terminal transfer when needed. Do not invent these values or a probability of making the connection.

For requested airport guidance, resolve the airport from the itinerary and use `byair_get_airport` and `byair_get_airport_tips`. Describe tips as community advice rather than guaranteed current operating information. Flightboard data is useful for a requested airport overview, not a substitute for the selected flight's detail.

End with concrete items the user needs to check or act on, based on returned data. The briefing does not add flights, change notifications, skip check-in/boarding, or promise background monitoring. Use a write tool only with authorization for that specific change.
