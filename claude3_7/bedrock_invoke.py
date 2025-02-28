#!/usr/bin/env python3
"""
Enhanced Claude 3.7 Sonnet Reasoning Capability Demo

This script demonstrates how to leverage Anthropic Claude 3.7 Sonnet's reasoning
capabilities through Amazon Bedrock. It showcases:

- Proper AWS client configuration using environment variables
- Modern Python error handling with context managers
- Type hints for better code documentation
- Structured logging
- A more complex and interesting reasoning challenge

Requirements:
- boto3
- Python 3.8+
- Configured AWS credentials
"""

import json
import logging
from typing import Dict, List, Optional, Tuple, Any

import boto3
from botocore.exceptions import ClientError


def configure_logging() -> None:
    """Set up structured logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def create_bedrock_client(region_name: str = "us-east-1") -> Any:
    """
    Create and return a configured Amazon Bedrock runtime client.
    
    Args:
        region_name: AWS region for the Bedrock client
        
    Returns:
        Configured Bedrock runtime client
    """
    try:
        # Using default credentials from environment or AWS config
        session = boto3.Session(profile_name="data_reply")
        return session.client("bedrock-runtime", region_name=region_name)
    except Exception as e:
        logging.error(f"Failed to create Bedrock client: {e}")
        raise


def invoke_claude_reasoning(
    client: Any,
    prompt: str,
    reasoning_budget: int = 2000,
    model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
) -> Tuple[Optional[str], Optional[str]]:
    """
    Invoke Claude 3.7 Sonnet with reasoning capability enabled.
    
    Args:
        client: Configured Bedrock client
        prompt: User prompt to send to Claude
        reasoning_budget: Token budget for the reasoning step
        model_id: Bedrock model ID for Claude 3.7 Sonnet
        
    Returns:
        Tuple containing (reasoning_text, response_text)
    """
    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]

    reasoning_config = {
        "thinking": {
            "type": "enabled",
            "budget_tokens": reasoning_budget
        }
    }

    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            additionalModelRequestFields=reasoning_config
        )

        content_blocks = response["output"]["message"]["content"]

        reasoning_text = None
        response_text = None

        for block in content_blocks:
            if "reasoningContent" in block:
                reasoning_text = block["reasoningContent"]["reasoningText"]["text"]
            if "text" in block:
                response_text = block["text"]

        return reasoning_text, response_text

    except ClientError as e:
        logging.error(f"Bedrock API error: {e}")
        raise
    except KeyError as e:
        logging.error(f"Unexpected response structure: {e}")
        raise
    except Exception as e:
        logging.error(f"Unknown error during model invocation: {e}")
        raise


def main() -> None:
    """Execute the Claude reasoning demonstration."""
    configure_logging()
    logger = logging.getLogger("claude_reasoning_demo")
    
    try:
        # Complex ethical dilemma that benefits from reasoning
        chess_puzzle_prompt = """
        You're given a chess position with the following pieces:
        - White King on e1
        - White Rook on h1
        - White Pawns on a2, b2, c2, d2, f2, g2, h2
        - Black King on e8
        - Black Queen on d8
        - Black Rooks on a8 and f8
        - Black Bishops on c8 and g7
        - Black Knights on b8 and g8
        - Black Pawns on a7, b7, c7, d7, e7, f7, h7
        
        White has just moved pawn from e2 to e4. Find the best move for Black and explain your reasoning step by step.
        """
        
        logger.info("Initializing Bedrock client")
        client = create_bedrock_client()
        
        logger.info("Invoking Claude with reasoning enabled")
        reasoning, response = invoke_claude_reasoning(client, chess_puzzle_prompt)
        
        if reasoning and response:
            print("\n===== CLAUDE'S REASONING PROCESS =====")
            print(reasoning)
            print("\n===== CLAUDE'S FINAL RESPONSE =====")
            print(response)
        else:
            logger.warning("Received incomplete response from Claude")
            
    except Exception as e:
        logger.error(f"Failed to run demonstration: {e}")


if __name__ == "__main__":
    main()