import boto3
from botocore.exceptions import ClientError

"""
This example demonstrates how to use Anthropic Claude 3.7 Sonnet's reasoning capability
with Amazon Bedrock. It shows how to:
- Set up the Amazon Bedrock runtime client
- Create a message
- Configure reasoning parameters
- Send a request with reasoning enabled
- Process both the reasoning output and final response
"""

def reasoning_example():
    # Create the Amazon Bedrock runtime client
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Specify the model ID. For the latest available models, see:
    # https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
    model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"

    # Create the message with the user's prompt
    user_message = "Describe the purpose of a 'hello world' program in one line."
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    # Configure reasoning parameters with a 2000 token budget
    reasoning_config = {
        "thinking": {
            "type": "enabled",
            "budget_tokens": 2000
        }
    }

    try:
        # Send message and reasoning configuration to the model
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            additionalModelRequestFields=reasoning_config
        )

        # Extract the list of content blocks from the model's response
        content_blocks = response["output"]["message"]["content"]

        reasoning = None
        text = None

        # Process each content block to find reasoning and response text
        for block in content_blocks:
            if "reasoningContent" in block:
                reasoning = block["reasoningContent"]["reasoningText"]["text"]
            if "text" in block:
                text = block["text"]

        return reasoning, text

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

if __name__ == "__main__":
    # Execute the example and display reasoning and final response
    reasoning, text = reasoning_example()
    print("\n<thinking>")
    print(reasoning)
    print("</thinking>\n")
    print(text)