from app.main import main


def test_main_runs_without_error(capsys):
    main()
    captured = capsys.readouterr()
    assert "Agentic Job Copilot" in captured.out
