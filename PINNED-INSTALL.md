# Pinned personal installation

Based on v0.4.1, commit `cf7572d29c1d9ea863e6c71290ba9b2d717542a9`.
Git origin is the owner's fork, `https://github.com/owenelliscodes/survival-llm.git`.
Do not fetch or merge upstream changes without the owner's explicit approval.

This fork removes app replacement code, daily/manual update checks, and update UI.
The library catalog is bundled from the reviewed commit, including asset hashes.
Environment variables cannot redirect either catalog or update checks.
Model pulls are disabled to prevent refreshing a mutable registry tag.
The prepared Granite 4.2 8B model files are verified against the captured manifest.

The native Mac launcher keeps settings, logs, personal files and models in `Data`
next to the app bundle. Its library is fixed at `Data/Library.noindex` for this self-contained installation.
Keep the app and `Data` together when moving this installation. The launcher uses
the bundled Ollama command-line engine on `127.0.0.1:11435`, disables cloud features,
and never launches a separately installed Ollama desktop app. Inference endpoints
must be loopback addresses. The engine may use its existing `~/.ollama` identity
files; model storage is separate and explicitly configured.

Build on Apple Silicon with Xcode Command Line Tools using `packaging/build.sh mac`.
Portable Python and Ollama archives are checked against fixed published SHA-256s.
Python package versions/hashes are in `packaging/requirements-mac.lock`; the build
installs only those wheels from `packaging/cache/wheels`, without network access
or source builds. `packaging/dependency-provenance.json` records wheel origins.
The source-only proxy_tools 0.1.0 wheel was built from the inspected, approved
source archive, SHA-256 `ccb3751f529c047e2d8a58440d86b205303cf0fe8146f784d1cbcd94f0a28010`.
Build tools are recorded separately in `packaging/build-tools.lock`.
Retain the dependency cache to reproduce this installation without new downloads.
The bundle records its source commit in `Contents/Resources/app/build-commit.txt`.

No upstream Survival LLM executable release is used. Python and Ollama are
verified third-party runtime binaries. Library data is a verified upstream
data archive. This does not guarantee absence of defects in those dependencies
or accuracy of generated medical advice.
