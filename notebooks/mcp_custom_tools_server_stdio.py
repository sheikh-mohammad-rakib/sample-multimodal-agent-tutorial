#!/usr/bin/env python3
"""
MCP Server for Custom Tools - stdio Transport
This server uses Standard I/O for process-to-process communication.

Built with FastMCP from Strands Agents ecosystem.
"""
import os
from datetime import datetime
from mcp.server import FastMCP

# Import video reader tool
from video_reader_local import video_reader_local

# Create FastMCP server
mcp = FastMCP("Custom Tools Server - stdio")


@mcp.tool(description="Performs basic mathematical operations (add, subtract, multiply, divide)")
def calculator(operation: str, a: float, b: float) -> str:
    """Calculator tool for basic math operations."""
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: Division by zero"
    }
    result = operations.get(operation, "Invalid operation")
    return str(result)


@mcp.tool(description="Gets the current date and time in UTC timezone")
def get_current_time(timezone: str = "UTC") -> str:
    """Get current date and time."""
    now = datetime.now()
    return f"Current time ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S')}"


@mcp.tool(description="Analyze video content using AWS Bedrock")
def analyze_video(
    video_path: str,
    text_prompt: str = "Describe what you see in this video",
    model_id: str = "us.amazon.nova-pro-v1:0",
    region: str = "us-west-2"
) -> str:
    """Analyze video content using AWS Bedrock."""
    result = video_reader_local(
        video_path=video_path,
        text_prompt=text_prompt,
        model_id=model_id,
        region=region
    )

    if result["status"] == "success":
        return result["content"][0]["text"]
    else:
        return result["content"][0]["text"]


# Run the server with stdio transport
if __name__ == "__main__":
    mcp.run(transport="stdio")  # Use stdio for command-line communication
