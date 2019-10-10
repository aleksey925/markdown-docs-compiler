# Скрипт для автоматической генерации базы знаний и заливки ее на gitbub
MODE=prod
export MODE
RESULT_DIR=`pwd`/result_dir/
python3 ./generator.py
cd $RESULT_DIR
git init
git add .
git commit -m 'init'
git remote add origin git@github.com:aleksey925/knowledge_base.git
git push -u origin master -f