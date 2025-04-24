"""Unit tests for hello_python module."""

from python.hello_python.module_python import main


def test_main(capsys):
    """Test that main function runs without errors and prints the expected message."""
    main()
    captured = capsys.readouterr()
    assert "Hello from Python" in captured.out