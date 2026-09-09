Добавить в переменные среды:
SMART_GIT_LLM_MODEL
SMART_GIT_LLM_HOST
SMART_GIT_LLM_USER
SMART_GIT_LLM_PASSWORD
NO_PROXY (равен SMART_GIT_LLM_USER)

python -m pip install -r requirements.txt

Сделай исполняемым:
chmod +x ~/.local/bin/git-ai-commit

Добавить в переменные среды PATH C:\Users\U_M27C4\.local\bin

Для преобразования в bash формат выполнить
sed -i 's/\r$//' ~/.local/bin/git-ai-commit
