#!/bin/bash
# Upload files into a github repo.
set -e

if [ $# -ne 3 ]; then
    echo "ERROR: needs two arguments. "
    echo "Sample usage:"
    echo "   $0 notebooks d2l-ai/notebooks version"
    exit -1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IN_DIR="$( cd $1 && pwd )"
REPO=$2
REPO_DIR=${IN_DIR}-git

# https://stackoverflow.com/questions/4846007/check-if-directory-exists-and-delete-in-one-command-unix/4848605
if [ -d "${REPO_DIR}" ]; then rm -Rf ${REPO_DIR}; fi
mkdir ${REPO_DIR}

# disabled git clone

# clone the repo, make sure GIT_USERNAME and GIT_PASSWORD have already set
# rm -rf ${REPO_DIR}


# https:
# git clone https://github.com/${REPO}.git ${REPO_DIR}
# OR ssh:
# git clone git@github.com:${REPO}.git ${REPO_DIR}

# remove all except for README.md and .git.
tmp=$(mktemp -d)

if [[ -f "${REPO_DIR}/README.md" ]]; then
    mv ${REPO_DIR}/README.md $tmp/
fi
# mv ${REPO_DIR}/.git $tmp/
rm -rf ${REPO_DIR}/*
if [[ -f "$tmp/README.md" ]]; then
    mv $tmp/README.md ${REPO_DIR}/
fi
# mv $tmp/.git ${REPO_DIR}/.git

cd ${REPO_DIR}
docs=$(mkdir docs -p)

cd ..

cp -r ${IN_DIR}/* ${REPO_DIR}/docs/


if [ -f ${REPO_DIR}/docs/index.html ]; then
    touch ${REPO_DIR}/docs/.nojekyll
fi

cd ..

cp -r _build/github_deploy-git/* .
rm -rf ${REPO_DIR}

git config --global push.default simple
git add -f --all .
# https://stackoverflow.com/questions/8482843/git-commit-bash-script
read -p "Commit description: " desc
git diff-index --quiet HEAD || git commit -am "$desc"
git push origin
