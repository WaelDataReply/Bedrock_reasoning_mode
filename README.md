# Enhanced Claude 3.7 Sonnet Reasoning Capability Demo

## Overview

This script demonstrates how to leverage Anthropic Claude 3.7 Sonnet's reasoning capabilities through Amazon Bedrock using an object-oriented approach. It includes:

- A `BedrockReasoningClient` class for interacting with the API
- Proper AWS client configuration using environment variables
- Modern Python error handling with context managers
- Type hints for better code documentation
- Structured logging
- A more complex and interesting reasoning challenge involving a chess puzzle

## Prerequisites

Ensure you have the following installed and configured before running the script:

- **Python 3.9+**
- **boto3 1.37.0+** (AWS SDK for Python)
- **AWS CLI** configured with valid credentials

## Installation

1. **Clone the repository**:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```sh
   pip install boto3
   ```

4. **Ensure AWS credentials are configured**:
   You must have AWS credentials set up with access to Amazon Bedrock.
   ```sh
   aws configure --profile data_reply
   ```

## Usage

To test the script, simply run:
```sh
python claude3_7/bedrock_reasoning_class.py
```
or 
```sh
python claude3_7/bedrock.py
```

### Expected Output
The script will:
- Initialize the `BedrockReasoningClient`
- Print model information
- Submit a complex chess puzzle prompt
- Display Claude's reasoning process and final response

## Troubleshooting

- **Invalid AWS credentials**: Ensure your AWS credentials are correctly configured using `aws configure`.
- **Missing boto3**: Run `poetry add boto3="^supported version` then `poetry install` to install the required package.
- **Bedrock API errors**: Verify that your AWS account has access to Amazon Bedrock and access to the model Claude Sonnet 3.7

## License

This project is licensed under the MIT License.

---

For any issues or contributions, feel free to submit a pull request or open an issue!

