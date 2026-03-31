# Bench-uperf

## Purpose
Scripts and configuration to run the uperf network performance benchmark within the crucible framework. Measures network throughput and latency using configurable protocols, message sizes, and thread counts.

## Languages
- Bash: client, server, and runtime scripts
- Perl: `uperf-post-process`

## Key Files
| File | Purpose |
|------|---------|
| `rickshaw.json` | Rickshaw integration: client/server scripts, parameter transformations |
| `multiplex.json` | Parameter validation rules, unit conversions, and presets for multiplex |
| `uperf-base` | Base setup: sources toolbox bench-base library |
| `uperf-client` | Client-side benchmark execution with configurable threads, protocol, sizes, duration |
| `uperf-server-start` / `uperf-server-stop` | Server lifecycle management |
| `uperf-get-runtime` | Extracts runtime from command-line options |
| `uperf-post-process` | Parses uperf results into CDM-compliant crucible metrics |
| `workshop.json` | Engine image build: compiles uperf from source |

## Conventions
- Primary branch is `master`
- Standard Bash/Perl modelines and 4-space indentation
