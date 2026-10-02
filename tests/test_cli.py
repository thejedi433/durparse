"""Tests for durparse CLI."""

import pytest
from durparse.cli import main


class TestCLI:
    """Tests for CLI main function."""
    
    def test_parse_duration(self, capsys, monkeypatch):
        monkeypatch.setattr('sys.argv', ['durparse', '1h'])
        assert main() == 0
        captured = capsys.readouterr()
        assert '3600.0' in captured.out
    
    def test_parse_combined(self, capsys, monkeypatch):
        monkeypatch.setattr('sys.argv', ['durparse', '1h30m'])
        assert main() == 0
        captured = capsys.readouterr()
        assert '5400.0' in captured.out
    
    def test_format_seconds(self, capsys, monkeypatch):
        monkeypatch.setattr('sys.argv', ['durparse', '-f', '3600'])
        assert main() == 0
        captured = capsys.readouterr()
        assert '1h' in captured.out
    
    def test_format_seconds_iso(self, capsys, monkeypatch):
        monkeypatch.setattr('sys.argv', ['durparse', '-f', '3600', '--iso'])
        assert main() == 0
        captured = capsys.readouterr()
        assert 'PT1H' in captured.out
    
    def test_invalid_duration_error(self, capsys, monkeypatch):
        monkeypatch.setattr('sys.argv', ['durparse', 'invalid'])
        assert main() == 1
        captured = capsys.readouterr()
        assert 'Error' in captured.err
    
    def test_no_args_error(self, capsys, monkeypatch):
        monkeypatch.setattr('sys.argv', ['durparse'])
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2


class TestCLIFormats:
    """Tests for different format parsing."""
    
    def test_iso_format(self, capsys, monkeypatch):
        monkeypatch.setattr('sys.argv', ['durparse', 'PT1H'])
        assert main() == 0
        captured = capsys.readouterr()
        assert '3600.0' in captured.out
    
    def test_human_format(self, capsys, monkeypatch):
        monkeypatch.setattr('sys.argv', ['durparse', '2d12h'])
        assert main() == 0
        captured = capsys.readouterr()
        assert '216000.0' in captured.out
