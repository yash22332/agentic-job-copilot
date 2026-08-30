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


async def search_jobs(
    query: str,
    location: str = "",
) -> list[dict[str, str]]:
    """Search jobs through the MCP server."""

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "search_jobs",
                {
                    "query": query,
                    "location": location,
                },
            )

            if result.is_error:
                error_messages = []

                for content in result.content:
                    if hasattr(content, "text"):
                        error_messages.append(content.text)

                raise RuntimeError(
                    "MCP job search failed: "
                    + " | ".join(error_messages)
                )

            structured = result.structured_content

            if not structured:
                return []

            return structured.get("result", [])


async def main() -> None:
    """Test the MCP job search client."""

    jobs = await search_jobs(
        query="Python",
        location="Bangalore",
    )

    print("Jobs found:")

    for job in jobs:
        print(job)


if __name__ == "__main__":
    asyncio.run(main())