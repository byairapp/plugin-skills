# byAir Agent Skills

Use byAir in Claude to check flights, prepare for trips, import itineraries and explore your flight history.

| Skill | What you can ask |
| --- | --- |
| `byair-flight-brief` | “Is my flight delayed? Where is the incoming plane?” |
| `byair-trip-brief` | “Brief me on my upcoming trip and connections.” |
| `byair-import-itinerary` | “Add the flights from this booking to byAir.” |
| `byair-flight-history` | “Which airlines did I fly last year?” |

## Requirements

Connect your byAir account through the byAir plugin or MCP connector in Claude. These skills use that connection to access your flights; they do not connect your account themselves.

## Install in Claude

1. Download this repository and open `skills/`.
2. ZIP each skill folder you want to use, keeping the folder itself at the archive root with `SKILL.md` inside.
3. In Claude, open **Customize → Skills**, upload each ZIP and enable it.

Ask naturally using the examples above, in your preferred language. Itinerary imports show a preview and ask for confirmation before adding flights to your account.
