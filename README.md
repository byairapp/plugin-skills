# byAir Agent Skills

The installable plugin is in [`plugins/byair/`](plugins/byair/). It contains the four skills, manifests for ChatGPT and Claude, the byAir MCP connection, its README, license and icon. See the [plugin README](plugins/byair/README.md) for requirements, supported workflows, privacy, support and manual installation.

## Directory source

For the Claude plugin bundle, use this repository, branch `main`, and plugin folder `plugins/byair`. Submit the remote MCP server as a separate connector.

OpenAI uses a ZIP built from the same plugin folder. The build scripts stay in `scripts/` outside the installable plugin and are developer utilities, not plugin runtime commands.

## Build and validate

Run from the repository root:

```sh
python3 scripts/package_plugin.py
python3 scripts/package_plugin.py --check
python3 scripts/package_skills.py
python3 scripts/package_skills.py --check
claude plugin validate ./plugins/byair
```

The OpenAI ZIP and standalone skill ZIPs are written to `dist/`. Keep reviewer credentials in private portal fields and out of repository files and archives.

## License

The skills and package are licensed under [MIT](LICENSE). Access to the hosted byAir service remains subject to its Terms and Pro subscription requirements.
