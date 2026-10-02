"""Parse duration strings to seconds and back."""

import re
from typing import Union

__version__ = "0.1.0"

# Duration units in seconds
UNITS = {
    'y': 365.25 * 86400,  # year (accounting for leap years)
    'w': 7 * 86400,       # week
    'd': 86400,           # day
    'h': 3600,            # hour
    'm': 60,              # minute
    's': 1,               # second
    'ms': 0.001,          # millisecond
}

# ISO 8601 duration pattern
ISO_PATTERN = re.compile(
    r'^P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)W)?(?:(\d+)D)?'
    r'(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$'
)

# Human-readable pattern (e.g., "1h30m", "2d 12h", "90s")
HUMAN_PATTERN = re.compile(
    r'(\d+(?:\.\d+)?)\s*([a-z]+)',
    re.IGNORECASE
)


def parse_to_seconds(duration: str) -> float:
    """Parse a duration string to seconds.
    
    Supports:
    - Human-readable: "1h30m", "2d 12h", "90s"
    - ISO 8601: "PT1H30M", "P1DT12H", "P1Y2M3DT4H5M6S"
    
    Args:
        duration: Duration string to parse
        
    Returns:
        Duration in seconds as float
        
    Raises:
        ValueError: If duration string is invalid
    """
    duration = duration.strip()
    if not duration:
        raise ValueError("Empty duration string")
    
    # Try ISO 8601 format
    if duration.upper().startswith('P'):
        return _parse_iso(duration)
    
    # Try human-readable format
    return _parse_human(duration)


def _parse_iso(duration: str) -> float:
    """Parse ISO 8601 duration format."""
    match = ISO_PATTERN.match(duration.upper())
    if not match:
        raise ValueError(f"Invalid ISO 8601 duration: {duration}")
    
    years, months, weeks, days, hours, minutes, seconds = match.groups()
    
    total = 0.0
    if years:
        total += int(years) * UNITS['y']
    if months:
        total += int(months) * 30.44 * 86400  # average month
    if weeks:
        total += int(weeks) * UNITS['w']
    if days:
        total += int(days) * UNITS['d']
    if hours:
        total += int(hours) * UNITS['h']
    if minutes:
        total += int(minutes) * UNITS['m']
    if seconds:
        total += float(seconds) * UNITS['s']
    
    return total


def _parse_human(duration: str) -> float:
    """Parse human-readable duration format."""
    matches = HUMAN_PATTERN.findall(duration)
    if not matches:
        raise ValueError(f"Invalid duration format: {duration}")
    
    # Verify the entire string was consumed
    reconstructed = ''.join(f"{val}{unit}" for val, unit in matches)
    if re.sub(r'\s+', '', duration).lower() != reconstructed.lower():
        raise ValueError(f"Invalid duration format: {duration}")
    
    total = 0.0
    for value, unit in matches:
        unit_lower = unit.lower()
        if unit_lower not in UNITS:
            raise ValueError(f"Unknown unit '{unit}' in duration")
        total += float(value) * UNITS[unit_lower]
    
    return total


def format_duration(seconds: float, style: str = 'human') -> str:
    """Format seconds as a duration string.
    
    Args:
        seconds: Duration in seconds
        style: 'human' (1h30m) or 'iso' (PT1H30M)
        
    Returns:
        Formatted duration string
        
    Raises:
        ValueError: If style is invalid or seconds is negative
    """
    if seconds < 0:
        raise ValueError("Duration cannot be negative")
    
    if style not in ('human', 'iso'):
        raise ValueError(f"Unknown style: {style}")
    
    # Break down into components
    years = int(seconds // UNITS['y'])
    seconds -= years * UNITS['y']
    
    days = int(seconds // UNITS['d'])
    seconds -= days * UNITS['d']
    
    hours = int(seconds // UNITS['h'])
    seconds -= hours * UNITS['h']
    
    minutes = int(seconds // UNITS['m'])
    seconds -= minutes * UNITS['m']
    
    secs = seconds
    
    if style == 'human':
        parts = []
        if years:
            parts.append(f"{years}y")
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if secs or not parts:
            if secs == int(secs):
                parts.append(f"{int(secs)}s")
            else:
                parts.append(f"{secs:.2f}s")
        return ''.join(parts)
    
    else:  # iso
        parts = ['P']
        if years:
            parts.append(f"{years}Y")
        if days:
            parts.append(f"{days}D")
        
        time_parts = []
        if hours:
            time_parts.append(f"{hours}H")
        if minutes:
            time_parts.append(f"{minutes}M")
        if secs:
            if secs == int(secs):
                time_parts.append(f"{int(secs)}S")
            else:
                time_parts.append(f"{secs:.2f}S")
        
        if time_parts:
            parts.append('T')
            parts.extend(time_parts)
        
        if len(parts) == 1:  # Only 'P'
            return 'PT0S'
        
        return ''.join(parts)
