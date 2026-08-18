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


async def main() -> None:
    """Connect to the MCP server and call a tool."""

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}")

            result = await session.call_tool(
                "get_company_info",
                {"company_name": "IBM"},
            )

            print("\nTool result:")
            for content in result.content:
                if hasattr(content, "text"):
                    print(content.text)


if __name__ == "__main__":
    asyncio.run(main())