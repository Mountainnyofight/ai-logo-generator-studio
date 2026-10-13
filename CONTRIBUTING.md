# Contributing to ai-logo-generator-studio

Thanks for wanting to plug into the studio. This repo is a **plugin host**:
the core is small, and almost every non-trivial feature lives in a plugin.

## Repo layout

```
src/ai_logo_studio/     # host runtime: bootstrap, loader, registry, pipeline
src/logo_kernels/       # diffusion + vectorizer kernels (native accel hooks)
src/plugins/            # first-party extension modules
src/shared_contracts/   # pydantic contracts shared by host <-> plugins
cmd/                    # CLI entrypoints
tests/                  # pytest suites (host + plugin contract tests)
config/                 # default pipelines, palettes, model routing
```

## Adding a plugin

1. Drop a package under `src/plugins/<your_plugin>/`.
2. Implement `LogoPlugin` from `shared_contracts.plugin`.
3. Declare your `PLUGIN_MANIFEST` with `name`, `version`, `capabilities`.
4. Register via the `ai_logo_studio.plugins` entry-point group **or** by placing
   a `manifest.toml` in a watched directory.
5. Run `logo-studio plugins list` to confirm the host picked it up.

Plugin contract tests run in `tests/test_plugin_contract.py`. If your plugin
fails the contract, the loader quarantines it instead of crashing the host.

## Native acceleration

`src/logo_kernels/native/` holds optional C++ / C# / Java shims for the
vectorizer and rasterizer. They are loaded lazily via `ctypes` / `pythonnet` /
`py4j`. If the shim isn't present, the host falls back to the pure-Python path.
Build instructions live in `src/logo_kernels/native/README`.

## Style

- `ruff` for lint, `black` for format, `mypy --strict` for the host package.
- Plugins may relax mypy to `--ignore-missing-imports`.
- No plugin may import another plugin directly — go through the registry.

## PRs

- One plugin per PR when possible.
- Include a snapshot test: `tests/snapshots/<plugin>_<case>.png`.
- Describe the capability you add and the fallback when it's absent.