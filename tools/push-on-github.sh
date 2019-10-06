# Скрипт для автоматической генерации базы знаний и заливки ее на gitbub
result_dir=`pwd`/result_dir/
MODE=prod
export MODE
python3 ./generator.py
cd $result_dir
git init
git add .
git commit -m 'init'
git remote add origin git@github.com:aleksey925/knowledge_base.git
git push -u origin master -f