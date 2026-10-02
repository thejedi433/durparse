"""durparse CLI."""

import argparse
import sys
from .parser import parse_to_seconds, format_duration


def main():
    """Main entry point for durparse CLI."""
    parser = argparse.ArgumentParser(
        description="Parse duration strings to seconds and back",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  durparse 1h30m          # Convert to seconds
  durparse PT1H30M        # ISO 8601 to seconds
  durparse -f 3600        # Format seconds to human-readable
  durparse -f 3600 --iso  # Format seconds to ISO 8601
"""
    )
    
    parser.add_argument(
        'duration',
        nargs='?',
        help="Duration string to parse (e.g., 1h30m, PT1H30M)"
    )
    
    parser.add_argument(
        '-f', '--format',
        type=float,
        metavar='SECONDS',
        help="Format seconds as duration string"
    )
    
    parser.add_argument(
        '--iso',
        action='store_true',
        help="Output in ISO 8601 format (with -f)"
    )
    
    args = parser.parse_args()
    
    # Format mode
    if args.format is not None:
        style = 'iso' if args.iso else 'human'
        print(format_duration(args.format, style))
        return 0
    
    # Parse mode
    if args.duration is None:
        parser.error("duration is required")
    
    try:
        seconds = parse_to_seconds(args.duration)
        print(seconds)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
