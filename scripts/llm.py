import os
import httpx
import requests

from errors import AuthError
from langchain_openai import ChatOpenAI


def get_token() -> str:
    try:
        host = os.environ.get('SMART_GIT_LLM_HOST')
        response = requests.post(
            f'https://{host}/login',
            data={'username': os.environ.get('SMART_GIT_LLM_USER'), 'password': os.environ.get('SMART_GIT_LLM_PASSWORD')},
            timeout=20,
            verify=False
        )
        response.raise_for_status()
        return response.json()['access_token']
    except Exception as e:
        raise AuthError(
            "Authentication failed",
            step='auth',
            cause=e,
        ) from e
    
    
def request(prompt):
    model = os.environ.get('SMART_GIT_LLM_MODEL')
    proxy = os.environ.get('SMART_GIT_LLM_HOST')
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
