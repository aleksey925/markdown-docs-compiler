python3 $BASE_DIR/generator.py
cd $RESULT_ROOT_DIR
git config --global user.email "ci@ci.com"
git config --global user.name "ci user"
git init
git add .
git commit -m 'init'
git remote add origin https://$GITHUB_USER:$GITHUB_TOKEN@github.com/aleksey925/knowledge-base.git
git push -u origin master -f