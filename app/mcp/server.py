"""
MCP server for Agentic Job Copilot tools.
"""

from mcp.server import MCPServer


mcp = MCPServer("Job Copilot Tools")


@mcp.tool()
def get_company_info(company_name: str) -> str:
    """
    Return basic company information.

    Args:
        company_name: Name of the company to look up.

    Returns:
        Basic company information.
    """

    companies = {
        "IBM": (
            "IBM is a technology company focused on cloud computing, "
            "AI, software, and enterprise technology."
        ),
        "Microsoft": (
            "Microsoft is a technology company focused on software, "
            "cloud computing, AI, and developer platforms."
        ),
    }

    return companies.get(
        company_name,
        f"No company information is available for {company_name}.",
    )


if __name__ == "__main__":
    mcp.run()
    