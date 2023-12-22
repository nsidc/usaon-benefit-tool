---
title: "Contributing Markdown"
---

In this tutorial, we will:

* Launch the GitHub.dev browser-based editor
* Create a branch
* Edit file(s)
* Make commit(s)
* Open a Pull Request (PR)

All without leaving the browser. This includes a rich editing experience with real-time
Markdown previews!


## Where are the Markdown files?

Markdown exists in two places for this app:

1. In the documentation: This documetation is separate from the Benefit Tool
   application, mainly for use by developers and project managers.
   * Lives in
     [the `doc/` directory](https://github.com/nsidc/usaon-benefit-tool/tree/main/doc).
   * Rendered by Quarto, so
     [supports some additional features on top of Markdown](https://quarto.org/docs/authoring/markdown-basics.html).
   * Deployed by ReadTheDocs, which includes Pull Request previews! This is the most
     user-friendly experience.
2. Built in to the app: This application is for use by the Benefit Tool's end-users
   (respondents and analysts) to aid them in using the app.
   * Lives in the
   [Jinja templates directory (`usaon_benefit_tool/templates/`)](https://github.com/nsidc/usaon-benefit-tool/tree/main/usaon_benefit_tool/templates).
   * Rendered by Python Markdown library.
     Follows the
     [standard Markdown syntax](https://www.markdownguide.org/basic-syntax/).
   * Must be released with a new version of the Benefit Tool and deployed by NSIDC
     dev/ops.

Markdown in both locations can be edited in the same manner.


## GitHub.dev

:::{.callout-note}
This seems like the simplest approach from a quick look.
We should try it and see if we like it, otherwise keep looking for more straightforward workflow.
:::


### 1. Start GitHub.dev

First, visit [our repository on GitHub](https://github.com/nsidc/usaon-benefit-tool).
Next, press the `.` key (or `>` to open in a new tab, but your browser may block this
"pop-up"), and you should see an editor start to load.

![GitHub.dev after starting for the first time](/_assets/github-dev-fresh.png)

In the GitHub.dev editor, there are **3 important elements** for this tutorial:

![GitHub.dev with important UI elements highlighted](/_assets/github-dev-highlights.png){height="600px"}

:::{.callout-important}
1. The **File Explorer**
2. The **Branch Selector**
3. The **Source Control Menu**
:::


### 2. Create a branch

Click the **Branch Selector** and then select "**+ Create new branch...**".


![GitHub.dev branch selector menu, with "Create new branch" selected](/_assets/github-dev-create-branch.png)

:::{.callout-note}
"**Create new branch from...**" can be useful if you'd like to start working from a
branch other than the `main` branch.
:::

Give your branch a meaningful name, for example `docs-tutorial`.

:::{.callout-important}
Your branch should focus on a small change, like adding one tutorial, or adding a set of
related glossary entries.
:::

Check the **Branch Selector** to verify your branch is created and checked out:

![GitHub.dev branch selector with new branch selected](/_assets/github-dev-branch-selector-updated.png)


### 3. Edit files

Using the **File Explorer**, click on the file you'd like to edit. It will open in the
editor.

![GitHub.dev with open Markdown file](/_assets/github-dev-open-markdown.png)

Click the **Preview Toggle** (highlighted in next figure) to enable like Markdown
previewing.

![GitHub.dev **Markdown Preview Toggle** highlighted in red](/_assets/github-dev-markdown-preview-toggle.png)

![GitHub.dev preview enabled](/_assets/github-dev-markdown-preview.png)

Apply your edits. Once you've done this, you'll notice **3 important things**:

![GitHub.dev after edits are applied](/_assets/github-dev-after-edit.png)

:::{.callout-important}
1. The **File Explorer** indicates modified files with an `M`. **Verify only the
   intended files are modified.**
2. The **Branch Selector** indicates modification with an `*`. **Verify that you are on
   the intended branch and _not_ the `main` branch**.
3. The **Source Control Menu** indicates `1` file has changed.

You can continue to edit more files, but please keep in mind, **your changes are not
saved yet. _Save early, and save often_ by committing (next step).**
:::


### 4. Commit changes

Click the **Source Control Menu**. The blue badge on this button indicates how many
files have changed, and after you click you will see a complete listing of changed
files.

![GitHub.dev ready to commit and push changes, with a "diff" shown](/_assets/github-dev-ready-to-commit-and-push.png)

Where the **File Explorer** was, there is now a listing of changed files. In this
example, I've only changed one file, but I encourage you to repeat the editing process
in this tutorial to change multiple files and combine related changes into
[small atomic commits](https://www.aleksandrhovhannisyan.com/blog/atomic-git-commits/).

If you click on a file, it will show what's called a "**diff**". The red-highlighted content
is **removed** content, and the green-highlighted content is **added** content.

:::{.callout-important}
**Verify your changes look as you intended!**
:::


#### Click "Commit & Push"

A pop-up will warn you that you must specify a commit message to proceed. Writing
[good commit messages](https://cbea.ms/git-commit/) is important, because they help
future us understand what present us was doing, and more importantly, _why_.

:::{.callout-tip}
A good rule of thumb is to write a commit message by filling in the blank: "When
applied, this change will _blank_." For example, the commit message I will use for
adding the tutorial you are reading will be: `Add a tutorial about contributing docs
with github.dev`.
:::

![GitHub.dev commit and push menu with a commit message entered](/_assets/github-dev-commit-message.png)

**As soon as you click "Commit & Push", your change will be saved to GitHub.**

:::{.callout-tip}
You may repeat the edit and commit cycle to create as many commits as you like before
moving on to the next step, but please try to keep the pull request easy to review by
only including related changes.
:::


### 5. Open a Pull Request (PR)

![GitHub.dev "New Pull Request" button](/_assets/github-dev-new-pr-button.png)

Click the "New Pull Request" button, highlighted in the figure above.

:::{.callout-note}
This will open a strange pull request menu within GitHub.dev. I think that's probably
fine, but it's also an option to open the pull request within GitHub.com's New Pull
Request interface.
:::

![GitHub.dev "Create Pull Request" menu](/_assets/github-dev-create-pr.png){height="800px"}

Double-check the "base" branch is set correctly. Usually, you want it to be `main`, but
in my case I created my branch from another branch called
`hazelshapiro-docs-addtutorial`.

Enter a meaningfull Pull Request title, for example "Add new tutorial about contributing
documentation with GitHub.dev".

Enter a useful description, for example discussing why you made the decisions you made
in this change.

Verify "Files changed" and "commits" include the intended contents.

You can now click "**Create**" and your pull request will be opened! :tada:
