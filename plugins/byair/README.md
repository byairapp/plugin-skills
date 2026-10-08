# byAir Agent Skills

Use byAir in ChatGPT and Claude to check flights, prepare for trips, import itineraries and explore your recorded flight history. The package includes four skills and a connection to the remote byAir MCP server.

| Skill | What you can ask |
| --- | --- |
| `byair-flight-brief` | “Is my flight delayed? Where is the incoming plane?” |
| `byair-trip-brief` | “Brief me on my upcoming trip and connections.” |
| `byair-import-itinerary` | “Add the flights from this booking to byAir.” |
| `byair-flight-history` | “Which airlines did I fly last year?” |

## Requirements

An existing byAir account and an active byAir Pro subscription are required to run MCP tools. Create an account in the byAir mobile app on iOS or Android. Connect your account through the byAir plugin or MCP connector and complete the byAir OAuth sign-in and consent flow. The skills use that connection to access your flights.

The common MCP endpoint is `https://api.byairapp.com/mcp`. The package contains this public URL and uses OAuth; it does not contain a personal API key or reviewer credentials.

## What the connection does

The skills retrieve relevant flight, trip, airport and recorded-history data from byAir. An itinerary import previews matched flights and asks for confirmation before adding tracking. Requests to the byAir MCP service can include search terms, dates, flight or trip identifiers, statistics references, and parameters for the tracking changes or email exports you request. Results are returned to your AI assistant through that connection. An explicitly requested export is sent by byAir to the email address you provide; a share link is returned without automatically sending it to anyone. These skills do not run local commands, install software or invoke additional connectors.

Flight status and predictions may be incomplete or change. The skills distinguish scheduled, estimated and actual times, and use airport-local timestamps. A byAir itinerary or seat entry does not buy a ticket or change an airline reservation. These skills do not provide continuous background monitoring.

For setup and support, see [AI integration](https://byairapp.com/features/ai-integration/), [FAQ](https://byairapp.com/faq/) or email connect@byairapp.com. Read the [Privacy Policy and Terms](https://byairapp.com/privacy_and_terms/) for how byAir handles your data and the conditions of use.

## Install in Claude

1. Download this repository and open `plugins/byair/skills/`.
2. ZIP each skill folder you want to use, keeping the folder itself at the archive root with `SKILL.md` inside.
3. In Claude, open **Customize → Skills**, upload each ZIP and enable it.

Ask naturally using the examples above, in your preferred language. Itinerary imports show a preview and ask for confirmation before adding flights to your account.

## Directory packages

This folder is the installable plugin for both platforms:

- OpenAI uses the portable `plugin.json`, `mcp.json` and `skills/` package.
- Claude uses `.claude-plugin/plugin.json`, which declares the same remote MCP endpoint, and discovers skills in `skills/`.
- Each skill declares its OpenAI MCP dependency in `agents/openai.yaml`.

Directory publication is separate from manual skill installation. Submit the remote MCP server as a Claude connector and use `plugins/byair` as the plugin folder in the repository. Credentials belong only in private portal fields, not in this folder or an upload ZIP.

## License

The skills and package are licensed under [MIT](LICENSE). Access to the hosted byAir service remains subject to its Terms and Pro subscription requirements.
