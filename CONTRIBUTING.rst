CONTRIBUTING
''''''''''''

Yes, please! Feel free to contribute to the project.

I would be glad if you do!
There are only a few things to keep in mind.

This project follows PEP 8, with one exception
 - This project uses tabs instead of spaces. Please do not submit PRs refactoring this.

If there are more exceptions from it, which I don't know about it, please try to be consistent!
And please try to avoid to mix big style changes with feature changes!

Thanks! :-)


How to update the documentation
-------------------------------

The documentation lies on the branch `gh-pages`.

In order to build these, change into the folder `docs/` and run `make html`.
The files will be output into `docs/_build/`.
The relevant files are under `docs/_build/html/`.
These are the ones that are on the `gh-pages` branch.

The easiest way to update the documentation would be to:
 - `git clone https://github.com/Vaelor/python-mattermost-driver.git python-mattermost-driver-docs`
 - `cd python-mattermost-driver-docs`
 - `git checkout gh-pages`
 - `cp -r python-mattermostdriver/docs/_build/html/. python-mattermost-driver-docs/`
 - Check the changed files with `git status`
 - Add them and commit/push


