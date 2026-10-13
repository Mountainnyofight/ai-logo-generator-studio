# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.9.x   | yes       |
| < 0.9   | no        |

## Reporting a vulnerability

Open a private security advisory on GitHub, or email `security@ai-logo-studio.dev`.
Do **not** open a public issue for anything exploitable.

Include:
- affected version / commit
- a minimal repro (prompt, plugin, config)
- impact (host crash, arbitrary code via plugin loader, path traversal in
  the asset cache, model-deserialization issue)

## Threat model

The host runs **untrusted plugin code** in-process. That is by design for a
desktop tool, but it means:

- Plugins are only loaded from the configured `plugin_paths` and from
  installed entry-points. Directory watching is opt-in.
- `manifest.toml` is validated before import. A plugin with an unsigned
  manifest is quarantined, not executed.
- Model weights are loaded with `weights_only=True` on the torch path.
  `.safetensors` is preferred; pickle weights are rejected.
- The asset cache path is normalized and confined to `out/`. Traversal
  attempts are logged and dropped.

## Out of scope

- Prompt injection against the diffusion model (it's a logo generator, not
  an agent).
- Denial of service from a user-supplied GPU-heavy prompt on their own box.