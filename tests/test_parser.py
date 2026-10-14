"""Tests for durparse parser."""

import pytest
from durparse.parser import parse_to_seconds, format_duration


class TestParseToSeconds:
    """Tests for parse_to_seconds function."""
    
    def test_parse_human_hours(self):
        assert parse_to_seconds("1h") == 3600.0
        assert parse_to_seconds("2h") == 7200.0
    
    def test_parse_human_minutes(self):
        assert parse_to_seconds("1m") == 60.0
        assert parse_to_seconds("30m") == 1800.0
    
    def test_parse_human_seconds(self):
        assert parse_to_seconds("1s") == 1.0
        assert parse_to_seconds("90s") == 90.0
    
    def test_parse_human_combined(self):
        assert parse_to_seconds("1h30m") == 5400.0
        assert parse_to_seconds("2d12h") == 216000.0
        assert parse_to_seconds("1h30m15s") == 5415.0
    
    def test_parse_human_with_spaces(self):
        assert parse_to_seconds("1h 30m") == 5400.0
        assert parse_to_seconds("2d 12h 30m") == 217800.0
    
    def test_parse_human_case_insensitive(self):
        assert parse_to_seconds("1H") == 3600.0
        assert parse_to_seconds("1H30M") == 5400.0
        assert parse_to_seconds("2D") == 172800.0
    
    def test_parse_human_decimal(self):
        assert parse_to_seconds("1.5h") == 5400.0
        assert parse_to_seconds("2.5m") == 150.0
    
    def test_parse_iso_hours(self):
        assert parse_to_seconds("PT1H") == 3600.0
        assert parse_to_seconds("PT2H") == 7200.0
    
    def test_parse_iso_minutes(self):
        assert parse_to_seconds("PT1M") == 60.0
        assert parse_to_seconds("PT30M") == 1800.0
    
    def test_parse_iso_seconds(self):
        assert parse_to_seconds("PT1S") == 1.0
        assert parse_to_seconds("PT90S") == 90.0
    
    def test_parse_iso_combined(self):
        assert parse_to_seconds("PT1H30M") == 5400.0
        assert parse_to_seconds("P1DT12H") == 129600.0
        # P1Y2M3DT4H5M6S = 1Y + 2M + 3D + 4H + 5M + 6S
        expected = 31557600 + 5260032 + 259200 + 14400 + 300 + 6
        assert parse_to_seconds("P1Y2M3DT4H5M6S") == pytest.approx(expected, rel=1e-3)
    
    def test_parse_iso_weeks(self):
        assert parse_to_seconds("P1W") == 604800.0
        assert parse_to_seconds("P2W") == 1209600.0
    
    def test_parse_iso_years(self):
        assert parse_to_seconds("P1Y") == pytest.approx(31557600.0, rel=1e-3)
    
    def test_parse_empty_raises(self):
        with pytest.raises(ValueError, match="Empty duration"):
            parse_to_seconds("")
    
    def test_parse_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="Empty duration"):
            parse_to_seconds("   ")
    
    def test_parse_invalid_format_raises(self):
        with pytest.raises(ValueError, match="Invalid duration"):
            parse_to_seconds("abc")
    
    def test_parse_malformed_duration_raises(self):
        # This passes regex but fails reconstruction check (line 96)
        with pytest.raises(ValueError, match="Invalid duration"):
            parse_to_seconds("1h2")
    
    def test_parse_unknown_unit_raises(self):
        with pytest.raises(ValueError, match="Unknown unit"):
            parse_to_seconds("1x")
    
    def test_parse_invalid_iso_raises(self):
        with pytest.raises(ValueError, match="Invalid ISO"):
            parse_to_seconds("P1H")  # Missing T for time
    
    def test_parse_leading_trailing_whitespace(self):
        assert parse_to_seconds("  1h  ") == 3600.0
        assert parse_to_seconds("\t1h30m\n") == 5400.0


class TestFormatDuration:
    """Tests for format_duration function."""
    
    def test_format_human_seconds(self):
        assert format_duration(1) == "1s"
        assert format_duration(90) == "1m30s"
    
    def test_format_human_minutes(self):
        assert format_duration(60) == "1m"
        assert format_duration(3600) == "1h"
    
    def test_format_human_hours(self):
        assert format_duration(3600) == "1h"
        assert format_duration(7200) == "2h"
    
    def test_format_human_days(self):
        assert format_duration(86400) == "1d"
        assert format_duration(172800) == "2d"
    
    def test_format_human_combined(self):
        assert format_duration(5400) == "1h30m"
        assert format_duration(90061) == "1d1h1m1s"
    
    def test_format_human_decimal_seconds(self):
        result = format_duration(1.5)
        assert result == "1.50s"
    
    def test_format_iso_seconds(self):
        assert format_duration(1, 'iso') == "PT1S"
        assert format_duration(90, 'iso') == "PT1M30S"
    
    def test_format_iso_minutes(self):
        assert format_duration(60, 'iso') == "PT1M"
        assert format_duration(3600, 'iso') == "PT1H"
    
    def test_format_iso_hours(self):
        assert format_duration(3600, 'iso') == "PT1H"
        assert format_duration(7200, 'iso') == "PT2H"
    
    def test_format_iso_days(self):
        assert format_duration(86400, 'iso') == "P1D"
        assert format_duration(172800, 'iso') == "P2D"
    
    def test_format_iso_combined(self):
        assert format_duration(5400, 'iso') == "PT1H30M"
        assert format_duration(90061, 'iso') == "P1DT1H1M1S"
    
    def test_format_iso_zero(self):
        assert format_duration(0, 'iso') == "PT0S"
    
    def test_format_human_zero(self):
        assert format_duration(0) == "0s"
    
    def test_format_human_years(self):
        # Test years formatting (line 145)
        assert format_duration(31557600) == "1y"
        assert format_duration(63115200) == "2y"
        assert format_duration(31557600 + 86400) == "1y1d"
    
    def test_format_negative_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            format_duration(-1)
    
    def test_format_invalid_style_raises(self):
        with pytest.raises(ValueError, match="Unknown style"):
            format_duration(100, 'invalid')
    
    def test_format_iso_years(self):
        result = format_duration(31557600, 'iso')
        assert result == "P1Y"
    
    def test_format_iso_decimal_seconds(self):
        # Test decimal seconds in ISO format (line 175)
        assert format_duration(1.5, 'iso') == "PT1.50S"
        assert format_duration(30.75, 'iso') == "PT30.75S"
