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
                raise RuntimeError("MCP job search failed")

            structured = result.structured_content

            if not structured:
                return []

            return structured.get("result", [])

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

            for content in result.content:
                if hasattr(content, "text"):
                    import json

                    return json.loads(content.text)

    return []

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


# async def main() -> None:
#     """Test the MCP client."""

#     info = await get_company_info("IBM")
#     print(info)
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

