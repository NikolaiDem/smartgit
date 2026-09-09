import subprocess

from commit_analyzer import CommitAnalyzer
from diff2msg import generate_commit_message, generate_better_commit_message
from errors import GittedError


MAX_RETRIES = 6
MIN_SCORE = 6


def run_git(*args):
    try:
        return subprocess.run(
            ["git", *args],
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=True,
        ).stdout
    except subprocess.CalledProcessError as error:
        print("Git error:")
        print(error.stderr)
        raise


def get_task_number():
    branch = run_git("branch", "--show-current")
    parts = branch.strip().split("/")
    if len(parts) < 2:
        return branch.strip()
    return parts[1]


def get_diff():
    run_git("add", ".")
    diff = run_git("diff", "--staged")
    # Remove invalid Unicode surrogate characters.
    return "".join(
        char for char in diff
        if not 0xD800 <= ord(char) <= 0xDFFF
    )


def generate_message(diff):
    print("Generate commit message")
    message = generate_commit_message(diff)
    message = message.splitlines()[-1]
    print(f"Generated: {message}")
    return message


def improve_message(message, analyzer):
    analysis = analyzer.analyze(message)
    score = int(analysis["score"])
    advice = analysis["response"]
    print(f"RESP: {advice}")
    print(f"SCORE: {score}")
    return score, advice


def generate_best_message(diff, message, analyzer):
    score, advice = improve_message(message, analyzer)
    retry = 0
    while score < MIN_SCORE and retry < MAX_RETRIES:
        print(f"Current score: {score}. New attempt")
        message = generate_better_commit_message(diff, message, advice)
        if "think" in message:
            message = message.splitlines()[-1]
        print(f"Generated: {message}")
        score, advice = improve_message(message, analyzer)
        retry += 1
    print(f"Final score: {score}")
    return message


def commit(message):
    task_number = get_task_number()
    commit_message = f"{task_number}: {message}"
    print(f"Commit: {commit_message}")
    run_git("commit", "-m", commit_message)
    #run_git("push")


def prepare():
    try:
        diff = get_diff()
        if not diff.strip():
            print("No changes to commit")
            return
        print(f"Diff size: {len(diff)} characters")
        analyzer = CommitAnalyzer()
        message = generate_message(diff)
        message = generate_best_message(diff, message, analyzer)
        commit(message)

    except GittedError as error:
        print(f"ERROR: {error}")
        raise

    except Exception as error:
        print(
            f"ERROR: [step=prepare] "
            f"Unexpected error: {type(error).__name__}: {error}"
        )
        raise


if __name__ == "__main__":
    prepare()
