"""
MCP client for Agentic Job Copilot.
"""

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="python",
    args=["app/mcp/server.py"],
)


async def get_company_info(company_name: str) -> str:
    """Call the MCP company information tool."""

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "get_company_info",
                {"company_name": company_name},
            )

            for content in result.content:
                if hasattr(content, "text"):
                    return content.text

    return "No company information returned."


async def main() -> None:
    """Test the MCP client."""

    info = await get_company_info("IBM")
    print(info)


if __name__ == "__main__":
    asyncio.run(main())