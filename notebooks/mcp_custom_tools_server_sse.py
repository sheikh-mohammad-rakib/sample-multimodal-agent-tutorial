#!/usr/bin/env python3
"""
MCP Server for Custom Tools
This server exposes calculator, time, and video analysis tools via Model Context Protocol.

Built with FastMCP from Strands Agents ecosystem.
"""
import os
from datetime import datetime
from mcp.server import FastMCP

# Import video reader tool
from video_reader_local import video_reader_local

# Create FastMCP server
mcp = FastMCP("Custom Tools Server")


@mcp.tool(description="Performs basic mathematical operations (add, subtract, multiply, divide)")
def calculator(operation: str, a: float, b: float) -> str:
    """
    Calculator tool for basic math operations.

    Args:
        operation: The operation to perform (add, subtract, multiply, divide)
        a: First number
        b: Second number

    Returns:
        The result of the operation as a string
    """
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
    """
    Get current date and time.

    Args:
        timezone: Timezone (currently only UTC supported)

    Returns:
        Current date and time as a formatted string
    """
    now = datetime.now()
    return f"Current time ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S')}"


@mcp.tool(description="""Analyze video content using AWS Bedrock's multimodal capabilities.

IMPORTANT LIMITATIONS:
- Only 1 video per request
- No audio analysis (visual only)
- Cannot identify people
- Maximum file size: ~20MB
- Supported formats: mp4, mov, avi, mkv, webm
""")
def analyze_video(
    video_path: str,
    text_prompt: str = "Describe what you see in this video",
    model_id: str = "us.amazon.nova-pro-v1:0",
    region: str = "us-west-2"
) -> str:
    """
    Analyze video content using AWS Bedrock.

    Args:
        video_path: Path to local video file
        text_prompt: Question or instruction for analyzing the video
        model_id: Bedrock model ID to use
        region: AWS region for Bedrock

    Returns:
        Video analysis results as a string
    """
    # Call the video reader tool
    result = video_reader_local(
        video_path=video_path,
        text_prompt=text_prompt,
        model_id=model_id,
        region=region
    )

    # Extract text from result
    return result["content"][0]["text"]


# Run the server
if __name__ == "__main__":
    mcp.run(transport="sse") # Use SSE for remote communication
