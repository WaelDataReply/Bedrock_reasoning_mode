import pytest
from unittest.mock import MagicMock, patch
from claude3_7.bedrock_reasoning_class import BedrockReasoningClient, configure_logging
import botocore


@pytest.fixture
def mock_boto3_session():
    with patch('boto3.Session') as mock_session:
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        # Add this line to mock the bedrock-runtime service
        mock_session.return_value.client.side_effect = lambda service_name, **kwargs: mock_client if service_name == 'bedrock-runtime' else MagicMock()
        yield mock_client

def test_create_client(mock_boto3_session):
    client = BedrockReasoningClient()
    assert client.client == mock_boto3_session

def test_get_model_info():

    try:
        client = BedrockReasoningClient()
        model_info = client.get_model_info()
        assert isinstance(model_info, dict)
    except botocore.exceptions.UnknownServiceError as e:
        pytest.fail(f"UnknownServiceError: {e}. Check if 'bedrock-runtime' is available in your region and boto3 version.")

def test_invoke_reasoning_success(mock_boto3_session):
    mock_boto3_session.converse.return_value = {
        "output": {
            "message": {
                "content": [
                    {"reasoningContent": {"reasoningText": {"text": "Reasoning"}}},
                    {"text": "Response"}
                ]
            }
        }
    }
    
    client = BedrockReasoningClient()
    reasoning, response = client.invoke_reasoning("Test prompt")
    
    assert reasoning == "Reasoning"
    assert response == "Response"
    mock_boto3_session.converse.assert_called_once()

def test_invoke_reasoning_error(mock_boto3_session):
    mock_boto3_session.converse.side_effect = Exception("API Error")
    
    client = BedrockReasoningClient()
    with pytest.raises(Exception):
        client.invoke_reasoning("Test prompt")

def test_configure_logging():
    with patch('logging.basicConfig') as mock_basic_config:
        configure_logging()
        mock_basic_config.assert_called_once()