def generate_dummy_response(brands):
    dummy_response = {}
    for brand in brands:
        dummy_response[brand] = {
            "Mention_YN": "Article not analysed, error generating response from OpenAI",
            "Corporate_Consumer": "",
            "Sentiment": "",
            "Sentiment_explanation": "",
            "Prominence": "",
            "Topics": "",
            "Spokespeople": "",
            "Positive_Brand_Values": "",
            "Negative_Brand_Values": "",
            "Story": ""
        }
    return dummy_response

def generate_dummy_response_2():
    dummy_response = {
                        "id": "chatcmpl-abc123",
                        "object": "chat.completion",
                        "created": 1677858242,
                        "model": "gpt-3.5-turbo-0613",
                        "usage": {
                            "prompt_tokens": 13,
                            "completion_tokens": 7,
                            "total_tokens": 20
                        },
                        "choices": [
                            {
                                "message": {
                                    "role": "assistant",
                                    "content": ('{"Mention_YN": "Article not analysed, error generating response from OpenAI", "Corporate_Consumer": "", "Sentiment": "", "Sentiment_explanation": "", "Prominence": "", "Topics": "", "Spokespeople": "", "Positive_Brand_Values": "", "Negative_Brand_Values": "", "Story": ""}')
                                },
                                "finish_reason": "stop",
                                "index": 0
                            }
                        ]
                    }
    return dummy_response