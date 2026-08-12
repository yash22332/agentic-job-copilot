
from app.main import main


def test_main_runs_without_error(capsys):
    """The application should run and print a resume analysis."""
    
    main()

    captured = capsys.readouterr()

    assert "Resume Analysis:" in captured.out
    assert "Yash Gupta" in captured.out