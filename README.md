# TermSquad remote MCP

![TermSquad](assets/termsquad-logo.png)

Free, MIT-licensed integration for Codex, Claude Code and Cursor. A TermSquad
account and an ACTIVE computer are required; the SaaS subscription is separate.
All clients use one OAuth-protected Streamable HTTP server:
`https://mcp.termsquad.com/mcp`.

**Release status:** package under validation. Clean local plugin installs passed in Codex and Claude Code; canonical portable JSON schemas and Claude manifests passed validation. The production endpoint and native OAuth in Codex, Claude Code and Cursor have passed, together with scoped reads, refresh rotation and revocation. Production one-shots and file mutations have passed. The native approval listener is active: a real SDK client passed human allow-once and a separate client-timeout cancellation, with owned cleanup. A Squad lead task also completed. Full Squad/debate and Schedule completion, proprietary-client elicitation UI coverage, Cursor desktop plugin installation and official listings remain pending. Do not interpret these instructions as an
approved marketplace listing.

## Install from GitHub

The public package is [termsquad/termsquad-plugin](https://github.com/termsquad/termsquad-plugin).
Install its own marketplace in Codex:

```bash
codex plugin marketplace add termsquad/termsquad-plugin
codex plugin add termsquad@termsquad
codex plugin list
```

In Claude Code:

```bash
claude plugin marketplace add termsquad/termsquad-plugin
claude plugin install termsquad@termsquad
claude plugin list
```

Connect through the client's MCP settings to complete OAuth. These are TermSquad's
own marketplace entries; official curated listings require separate review.

## Local plugin installation

Clone or copy this directory without adding tokens or credentials.

- **Codex:** run `codex plugin marketplace add /absolute/path/to/termsquad-plugin`,
  then `codex plugin add termsquad@termsquad`. Verify with `codex plugin list`.
  These commands were tested with an isolated profile.
- **Claude Code:** run `claude --plugin-dir /absolute/path/to/termsquad-plugin`.
  Use `/mcp` to authenticate. For a local marketplace, run
  `/plugin marketplace add /absolute/path/to/termsquad-plugin`, then
  `/plugin install termsquad@termsquad`.
- **Cursor:** this package uses the root Agent Plugins format documented by
  Cursor. The installed Cursor Agent CLI here does not expose plugin installation;
  desktop plugin installation remains unverified. Use the direct MCP configuration
  below until the package has passed desktop validation and marketplace review.

## Direct MCP connection

Codex:

```bash
codex mcp add termsquad --url https://mcp.termsquad.com/mcp
codex mcp login termsquad
```

Claude Code:

```bash
claude mcp add --transport http termsquad https://mcp.termsquad.com/mcp
```

Then use `/mcp` to authenticate. For Cursor, merge into `.cursor/mcp.json`:

```json
{"mcpServers":{"termsquad":{"url":"https://mcp.termsquad.com/mcp"}}}
```

Connect from Cursor's MCP settings. The browser sign-in uses TermSquad, followed
by a dedicated **Connect to TermSquad** page for every client. Read access is
selected by default; choose the computer/workspaces and expand **Access permissions**
to allow execution or changes. Each client has a separate revocable connection,
not a different authentication system. Never paste a TermSquad
session cookie, machine token, private key or provider credential into a plugin.

Try: “List my authorized TermSquad computers and workspaces.” Then request a
specific task in a selected workspace. Temporary executions return a handle;
poll it with `agent_wait` every five seconds. Polling keeps the authorization
lease alive. Cancel with `agent_stop`. A disconnected client loses the lease
and its temporary resources are cleaned up. Results expire and are not history.
Persistent agents and existing scheduled tasks use their separate tools.

Keep the client waiting while completing browser consent. If localhost reports
`ERR_CONNECTION_REFUSED`, its callback listener has stopped: start Connect again
in that client. An expired or already used authorization request cannot be reused.

Edit permissions or revoke access in **Settings → Integrations → MCP**.
Write scopes require explicit consent. File operations are bounded and use
revisions; hidden credential/configuration paths and symlinks are denied.
Outputs are untrusted agent output, not independently verified results.

TermSquad stores security metadata, not one-shot prompts, outputs or native
session references. Continue a conversation through the harness's own `/resume`;
TermSquad does not locate or guarantee that history.

## Publication

Only this integration directory is published to `termsquad/termsquad-plugin`.
Complete the remaining live acceptance checks before official submission. The public package contains
no backend, runtime binary, orchestration policy, npm wrapper or STDIO server.
The own marketplaces above are separate from official listings.

Official submission entry points:

- [OpenAI submission](https://developers.openai.com/plugins/deploy/submission)
- [Claude plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Cursor publish](https://cursor.com/marketplace/publish)

Official format references, checked 2026-10-13:
[OpenAI packaging](https://developers.openai.com/plugins/build/plugins),
[Agent Plugins schemas](https://agent-plugins.org),
[Claude manifests](https://code.claude.com/docs/en/plugins-reference),
[Cursor plugins](https://cursor.com/docs/reference/plugins),
[MCP authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization).

Some mutations return `human_approval_required`: file/task deletion and sensitive
Skills changes must be approved by you in TermSquad in normal mode. Open the returned link,
review the client and exact request, including its computer, workspace and target, then let the client resubmit the
identical request and action ID. Approval expires after ten minutes and cannot
be reused for changed arguments.


## Review native exceptions in your MCP client

When a remote Codex agent needs a permission exception, `agent_approval` opens a
human form in your connected MCP client. Review the exact command and destination
and choose deny or allow once. The tool cannot accept a model-provided decision.
The connection needs `agents:read` and `agents:manage` for that destination.

This requires a TermSquad Runtime with the native approval bridge, managed Codex
0.162.1 or newer with hooks enabled, and a client supporting MCP form elicitation.
The remote harness adapter currently covers Codex shell/patch exceptions. It does
not provide native Claude/Cursor approval adapters; those products may separately
act as MCP clients. Unsupported clients report `elicitation_not_supported`.
Cancellation, expiry and revocation cannot approve an action. File/task deletions
and sensitive Skills changes retain their authenticated TermSquad approval page in normal mode.

The bridge is deployed and the production SDK checks above passed. This
repository remains a prerelease: those checks do not certify marketplace
acceptance or the elicitation UI of every proprietary client.
The server contract contains the original 23 tools plus this additional tool.


## Optional YOLO mode

In the connection screen or **Settings → Integrations → MCP → Edit permissions**,
the user can enable **YOLO · Automatically approve all actions**. It is off by
default and includes agent approvals, deletions and sensitive MCP changes.
Permissions, workspace selection, revision checks and revocation still apply.
A client cannot enable it through a tool argument. Keep polling YOLO agents at
the returned interval; expired authorization closes their owned resources.

YOLO uses verified capabilities of the installed native harness; an unsupported
CLI fails explicitly. Manual Schedule runs use YOLO for that execution only;
saved recurring task settings remain unchanged. Provider login/trust still
belongs to the native harness. Production YOLO acceptance is pending the Runtime
listener update; this section documents the prepared integration.
