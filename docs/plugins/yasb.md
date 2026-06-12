# YASB Plugin

## Overview

The YASB plugin manages YASB configuration using its YAML configuration file.

## Prerequisites

- YASB installed
- PyYAML available
- User profile access

## Configuration Schema

| Key | Purpose |
|------|--------|
| settings | YAML configuration values to merge into `config.yaml` |

## Usage Examples

### Enable configuration watching

```yaml
plugins:
  - name: yasb
    settings:
      watch_config: true
      watch_stylesheet: true
```

### Configure bars

```yaml
plugins:
  - name: yasb
    settings:
      bars:
        status-bar:
          enabled: true
          widgets:
            left:
              - workspaces
              - active_window
            right:
              - cpu
              - memory
              - volume
              - battery
```

## Verification Steps

```bash
dir "%USERPROFILE%\.config\yasb"
```

Verify that `config.yaml` exists and contains the expected values.

## Notes / Caveats

- Existing YAML configuration is merged recursively.
- Dry-run previews are supported.
- Corrupted configuration files are backed up automatically.
- Missing configuration directories are created automatically.
- Configuration updates are written atomically.
