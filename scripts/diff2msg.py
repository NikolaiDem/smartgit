from llm import request

from errors import GenerationError


BASE_PROMPT = """
You are a programmer who cares about the quality of commit messages
in his repository.
You know how to write COMPACT and INFORMATIVE commit messages.
"""

COMMIT_MESSAGE_RULES = """
Return back just the commit message in English.
Take into account the changes of each class.
No additional explanations or meta information.
Just return one-sentence commit message, without quotation marks around.
Try to make it as short as possible, ideally under 80 characters.
Don't even finish it with a dot, just give me a single sentence.
"""


def _generate(prompt):
    print(f"Prompt: {prompt}")

    try:
        return request(prompt)
    except Exception as e:
        raise GenerationError(
            "Failed to generate commit message",
            step="generate",
            cause=e,
        ) from e


def generate_commit_message(diff):
    if not diff.strip():
        return "No changes"

    prompt = f"""
{BASE_PROMPT}

Now, study the changes made to a repository recently and suggest a good
commit message.
Let me show you the changes as they are printed by 'git diff':

```

{diff}

```

{COMMIT_MESSAGE_RULES}
"""

    return _generate(prompt)


def generate_better_commit_message(diff, message, advice):
    prompt = f"""
{BASE_PROMPT}

Now, improve my suggested commit message.

My suggested commit message:

```

{message}

```
"""

    if advice:
        prompt += f"""

Here is the recommendation for improving the commit message:
"{advice}"

Use this text as a source of inspiration.
"""

    if diff:
        prompt += f"""
        Let me show you the changes as they are printed by 'git diff':

```

{diff}

```
        """

    prompt += f"""

{COMMIT_MESSAGE_RULES}
"""

    return _generate(prompt)

