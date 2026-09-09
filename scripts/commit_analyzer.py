from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import httpx
import requests
import os
import re
import urllib3

from errors import AuthError, AnalysisError, ParseError
from llm import request

# Отключение предупреждений о небезопасном SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CommitAnalyzer:

    def __init__(self):
        pass

    def parse_response(self, response: str) -> dict:
        """Разбирает ответ модели и возвращает единую структуру результата.

        Возвращает словарь вида:
            {'ok': True, 'score': int, 'response': str, 'error': None}
        При неудачном разборе бросает ParseError.
        """
        try:
            score_match = re.search(
                r'Оценка.*?(\d+/10)|(\d+/10)',
                response,
                re.IGNORECASE | re.MULTILINE | re.DOTALL
            )

            score_str = (
                score_match.group(1)
                if score_match and score_match.group(1)
                else score_match.group(2)
                if score_match and score_match.group(2)
                else "0/10"
            ).split('/')[0]

            try:
                score = int(score_str)
            except ValueError as e:
                raise ParseError(
                    f"Non-numeric score '{score_str}' in model response",
                    step='parse',
                    cause=e,
                ) from e

            return {
                'ok': True,
                'score': score,
                'response': response,
                'error': None,
            }
        except ParseError:
            raise
        except Exception as e:
            raise ParseError(
                "Failed to parse model response",
                step='parse',
                cause=e,
            ) from e

    def analyze(self, commit_msg: str) -> dict:
        """Анализирует commit message и возвращает единую структуру результата.

        Возвращает словарь вида:
            {'ok': True, 'score': int, 'response': str, 'error': None}
        При ошибке анализа бросает AnalysisError.
        """
        try:
            messages = [
                SystemMessage(
                    content="""
                    You are an expert in commit message analysis.
                    Analyze the commit message strictly according to the criteria below and do not go beyond them:

                    1. Commit structure: presence of a task number at the beginning (for example, TASK-XXX), correct syntax, logical order of statements.
                    2. Completeness of change description: whether it clearly and sufficiently describes WHAT exactly was done. Do not explain WHY it was done.
                    3. Clarity and informativeness: the message should be easy to read and unambiguous.
                    4. Technical accuracy: correct use of technical terms, no errors.
                    5. Message length: the message should be balanced, not too short or excessively long.

                    When assigning a score:
                    - Base the score only on the meaningful content describing what was done.
                    - Do not increase the score for the presence of the task number (e.g., TASK-XXX). This is automatically added and should not affect the assessment.
                    - 1–2/10: very generic message, no details at all, extremely low informativeness.
                    - 3–4/10: generic message, minimal details, very low informativeness.
                    - 5–6/10: partial details present, but lacks specifics and clarity.
                    - 7–8/10: good details, mentions files, modules, parameters, but can still be improved.
                    - 9–10/10: excellent, fully clear, detailed, technically accurate, easy to read.
                    Important:
                    - In the recommendations section, always provide concrete ideas on how to improve the content of the commit message to make it more useful and informative. For example, suggest clarifying which parameters were changed or which files were affected.
                    - Do not suggest rewritten full versions of the commit message.
                    - Do not invent details that are not present in the commit message.
                    - Strictly follow the output format (GitLab format):

                    ## Quality Score: **X/10**

                    ## Main Comments:
                    ...

                    ## Recommendations for Improvement:
                    ...

                    **Example of an Improved Commit Message:**
                    > ...


                    Provide only the analysis, do not add introductory or concluding comments.

                    Rules (Best Practices):
                    - Strictly follow the specified output format without adding or removing sections.
                    - Do not add explanations of motivation or the impact of changes.
                    - In the recommendations, always suggest concrete content improvements rather than general advice.
                    - Do not suggest rewritten full versions of commit messages.
                    - Do not invent missing details.
                    - Indicate if the commit message is too short or excessively long.
                    - Use the English language for the final answer
                    - Check for correct structure (task number, optional type, brief description)."""),
                HumanMessage(content=commit_msg)
            ]
            response = request(messages)
            return self.parse_response(response)
        except (ParseError, AnalysisError):
            raise
        except Exception as e:
            raise AnalysisError(
                "Failed to analyze commit message",
                step='analyze',
                cause=e,
            ) from e
