# Credits to: https://executableopinions.readthedocs.io/en/latest/labs/gh-pages/gh-pages.html

SRCDOCS=$(readlink -f ./docs/_build/html)

echo $SRCDOCS

cd $SRCDOCS
MSG="Adding gh-pages docs for `git log -1 --pretty=short --abbrev-commit`"

TMPREPO=/tmp/docs/user
rm -rf $TMPREPO
mkdir -p -m 0755 $TMPREPO

git clone https://github.com/Vaelor/python-mattermost-driver.git $TMPREPO
cd $TMPREPO
git checkout gh-pages  ###gh-pages has previously one off been set to be nothing but html
rm -rf ./*
cp -r $SRCDOCS/* $TMPREPO
git add -A
git commit -m "$MSG" && git push origin gh-pages
