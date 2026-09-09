import os
import httpx

from langchain_openai import ChatOpenAI
from secret import get_token

def request(prompt):
    model = os.environ.get('MODEL')
    proxy = os.environ.get('LLM_HOST')
    if not proxy:
        return 'fix'

    client = ChatOpenAI(
        http_client=httpx.Client(verify=False),
        default_headers={'X-Model-Type': model},
        base_url=f'https://{proxy}/pcai',
        api_key=get_token(),
        model=model,
        temperature=0,
        extra_body={
            "chat_template_kwargs": {"enable_thinking": False},
        },
    )
    return client.invoke(prompt).content