# durparse

Parse duration strings to seconds and back.

## Installation

```bash
pip install durparse
```

## Usage

### Command Line

```bash
# Parse duration to seconds
durparse 1h30m          # 5400.0
durparse 2d 12h         # 216000.0
durparse PT1H30M        # 5400.0 (ISO 8601)

# Format seconds to duration
durparse -f 3600        # 1h
durparse -f 3661        # 1h1m1s
durparse -f 3600 --iso  # PT1H
```

### Python API

```python
from durparse import parse_to_seconds, format_duration

# Parse to seconds
parse_to_seconds("1h30m")      # 5400.0
parse_to_seconds("2d 12h")     # 216000.0
parse_to_seconds("PT1H30M")    # 5400.0

# Format from seconds
format_duration(5400)          # "1h30m"
format_duration(5400, 'iso')   # "PT1H30M"
```

## Supported Formats

- Human-readable: `1h30m`, `2d 12h`, `90s`, `1y 2d`
- ISO 8601: `PT1H30M`, `P1DT12H`, `P1Y2M3DT4H5M6S`

Units: y (year), w (week), d (day), h (hour), m (minute), s (second), ms (millisecond)

## License

MIT
