Title: MCP server configuration and /mcp command foundation
Files: src/cli.rs, src/commands.rs, src/help.rs
Issue: none

## Why

MCP (Model Context Protocol) is the biggest capability gap vs every major competitor. Claude Code, Gemini CLI, and Codex all support MCP servers. This task lays the foundation: config parsing and a `/mcp` command to list configured servers.

This is Task 1 of a multi-session MCP effort. Future sessions will implement the actual JSON-RPC protocol, tool discovery, and tool integration.

## What to Build

### 1. Config parsing in `cli.rs`

Add MCP server configuration parsing. The config format (in `.yoyo.toml` or `~/.config/yoyo/config.toml`) should support:

```toml
[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]

[mcp_servers.postgres]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-postgres"]
env = { DATABASE_URL = "postgresql://localhost/mydb" }
```

Add a struct:
```rust
#[derive(Debug, Clone)]
pub struct McpServerConfig {
    pub name: String,
    pub command: String,
    pub args: Vec<String>,
    pub env: Vec<(String, String)>,
}
```

Parse `[mcp_servers.*]` sections from the config TOML. Store them in `Config` as `pub mcp_servers: Vec<McpServerConfig>`. If no `[mcp_servers]` section exists, default to empty vec.

### 2. `/mcp` command in `commands.rs`

Add a `/mcp` slash command with subcommands:
- `/mcp` or `/mcp list` — list all configured MCP servers with their command and status (configured/not started)
- `/mcp help` — show how to configure MCP servers

Output format for `/mcp list`:
```
MCP Servers:
  filesystem  npx -y @modelcontextprotocol/server-filesystem /path
  postgres    npx -y @modelcontextprotocol/server-postgres

2 servers configured (not connected — MCP protocol support coming soon)
```

If no servers configured:
```
No MCP servers configured.

Add servers to .yoyo.toml:
  [mcp_servers.myserver]
  command = "npx"
  args = ["-y", "@modelcontextprotocol/server-example"]

See /mcp help for more details.
```

### 3. Help text in `help.rs`

Add `/mcp` to the help system with appropriate description: "List and manage MCP server connections"

### 4. Wire into command dispatch

Add "mcp" to `KNOWN_COMMANDS` in `commands.rs` and add the dispatch case in the main command handler (likely in `repl.rs` or wherever slash commands are dispatched).

## Tests

Add tests for:
1. `McpServerConfig` struct creation
2. Config parsing with MCP servers present
3. Config parsing with no MCP servers (empty vec)
4. Config parsing with env vars in MCP server config

All tests should be in the same file as the implementation (unit tests at bottom of `cli.rs` and/or `commands.rs`).

## Important Notes

- Do NOT implement the actual MCP protocol (JSON-RPC, initialize handshake, tool discovery). That's for future sessions.
- Do NOT spawn any processes. This is config + display only.
- Keep it simple — the goal is establishing the config schema and command structure.
- The "coming soon" message is intentional — it's honest about current capability.

## Documentation

- Add `/mcp` to the command list in `help.rs`
- No need to update CLAUDE.md or README.md yet — MCP isn't functional until the protocol is implemented.
