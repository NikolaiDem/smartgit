python -m pip install -r requirements.txt

nano ~/.local/bin/git-ai-commit
И положи туда:

#!/bin/bash

PYTHON=$(which python)

if [ -z "$PYTHON" ]; then
echo "Python не найден"
exit 1
fi

cd "$HOME/git-ai-commit" || exit 1

"$PYTHON" main.py "$@"

Сделай исполняемым:

chmod +x ~/.local/bin/git-ai-commit

Если ещё не добавлял:

Добавить в переменные среды PATH C:\Users\U_M27C4\.local\bin

Для преобразования в bash формат выполнить
sed -i 's/\r$//' ~/.local/bin/git-ai-commit
