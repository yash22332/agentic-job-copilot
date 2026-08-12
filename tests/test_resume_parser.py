from app.resume_parser import parse_resume


def test_parse_pdf_resume():
    """PDF parser should return non-empty text."""
    text = parse_resume("data/sample_resume.pdf")

    assert text
    assert "Yash Gupta" in text