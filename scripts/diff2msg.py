from llm import request

from errors import GenerationError


BASE_PROMPT = """
You are a programmer who cares about the quality of commit messages
in his repository.
You know how to write COMPACT and INFORMATIVE commit messages.
Use rules:
1. Completeness of change description: whether it clearly and sufficiently describes WHAT exactly was done. Do not explain WHY it was done.
2. Clarity and informativeness: the message should be easy to read and unambiguous.
3. Technical accuracy: correct use of technical terms, no errors.
4. Message length: the message should be balanced, not too short or excessively long.
5. Don't even finish it with a dot, just give me a single sentence.
6. Return back just the commit message in English.

This message will be scored by:
- 1–2/10: very generic message, no details at all, extremely low informativeness.
- 3–4/10: generic message, minimal details, very low informativeness.
- 5–6/10: partial details present, but lacks specifics and clarity.
- 7–8/10: good details, mentions files, modules, parameters, but can still be improved.
- 9–10/10: excellent, fully clear, detailed, technically accurate, easy to read.
Final score must be 6 and higher.
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
    return _generate(prompt)
