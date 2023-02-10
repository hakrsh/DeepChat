# DeepChat

DeepChat is a simple command-line chatbot powered by OpenAI, providing real-time Q&A with a user-friendly interface following Material Design guidelines.

![DeepChat Demo](demo.jpg)


## Getting Started
### Motivation
ChatGPT is fantastic, but the constant errors caused by high traffic are frustrating. That's why I thought about creating a custom CLI chatboot, based on OpenAI's GPT-3 API, which has less traffic compared to ChatGPT. To get started, you need to generate an API key from the OpenAI website and store it in a file called .env with the following format:
<br>
`OPENAI_API_KEY1=sk-C11pi...`


### Prerequisites

You'll need to generate an OpenAI API key and store it in your environment variables as `OPENAI_API_KEY`. You can do this by following the instructions on the OpenAI website.

You'll also need to create a virtual environment and install the required packages. You can do this by running the following commands:

```
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### Running the chatbot

To run the chatbot, simply run the following command in your terminal: `python deepchat.py`

The chatbot should start up, and you can start interacting with it.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [OpenAI](https://openai.com) for providing the API and tools to make this project possible.


