# Скачивает актуальную версию базы знаний из git репозитория с *.md файлами, конвертирует их в html и заливает их в
# специально подготовленный github репозиторий, где включена функция pages.
# Позволяет облегчить публикацию изменений при работе с локального ПК.
MODE=prod
RESULT_DIR=`pwd`/result_dir/
GITHUB_REPO=git@github.com:aleksey925/knowledge_base.git
export MODE

python3 ./generator.py
cd $RESULT_DIR
git init
git add .
git commit -m 'init'
git remote add origin $GITHUB_REPO
git push -u origin master -f
