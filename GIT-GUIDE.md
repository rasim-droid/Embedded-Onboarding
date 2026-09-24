```
████ TOP SECRET ████   GIT, FROM ZERO
```

Never used git? Start at step 1 and do every command. Nothing is assumed.

Used it before? You only need **step 4**: work in your own repository, created from the template, never in the original.

Every line starting with `$` is a command you type. Do not type the `$`.

---

## What git is, in four sentences

Git records snapshots of your files over time. Each snapshot is called a **commit**, and it has a message saying what changed.

GitHub is a website that stores a copy of your repository so other people (us) can see it. This project's repository is a **template**, so instead of cloning it directly, you click **Use this template** to generate your own brand new, independent repository with the same starting files.

For this project you create your own repository from the template and work there. You never push to the original, nobody else can see your repository unless you share it, and the finished project is yours to show off as your own.

---

## STEP 1: Install git

**Windows:** download from https://git-scm.com/download/win and run the installer. Accept every default. This also gives you "Git Bash", which is where you type these commands.

**macOS:** open Terminal and type `git --version`. If it is not installed, macOS offers to install it. Otherwise install Homebrew from https://brew.sh then:
```
$ brew install git
```

**Linux (Ubuntu/Debian):**
```
$ sudo apt update
$ sudo apt install git
```

Check it worked:
```
$ git --version
```
You should see something like `git version 2.43.0`.

---

## STEP 2: Tell git who you are

Do this once, ever. Your name and email go on every commit you make.

```
$ git config --global user.name "Your Name"
$ git config --global user.email "your.email@example.com"
```

Use the same email as your GitHub account or your commits will not link to your profile.

Check it:
```
$ git config --global --list
```

---

## STEP 3: Create your repository from the template, then clone it

**First create your repository.** This makes your own independent copy of the project under your GitHub account. 

1. Open the repository on GitHub. Your Handler will give you the link.
2. Click the green **Use this template** button near the top right, then **Create a new repository**.
3. Pick an owner (your account) and a name the default name is fine. Click **Create repository**.
4. GitHub takes you to `github.com/<YOUR-USERNAME>/<REPO>`. That page is your repository.

**Then clone it.** Cloning means downloading a full copy to your computer, history and all. On your repository's page, click the green **Code** button and copy the URL.

```
$ git clone https://github.com/<YOUR-USERNAME>/<REPO>.git
$ cd <REPO>
```

Replace `<YOUR-USERNAME>` with your GitHub username and `<REPO>` with the repository name. The URL must have your username in it, not the original organisation's.

**If it asks for a password:** GitHub stopped accepting account passwords in 2021. You need one of these:

- **Personal access token (easier).** Create one at https://github.com/settings/tokens, tick the `repo` scope, copy the token, and paste it when git asks for your password. Save it somewhere, GitHub will not show it again.
- **SSH key (nicer long term).** Follow https://docs.github.com/en/authentication/connecting-to-github-with-ssh then clone using the `git@github.com:...` URL instead.

---

## STEP 4: Check you are in your own repository

**This is the important one.** Everything you do is pushed to your own repository, never to the original.

```
$ git remote -v
```

You should see your own GitHub username in the URLs, like `github.com/alex-chen/<REPO>`.

> If you see the original organisation's name instead of your username, you cloned the original by accident. Stop, and follow "I cloned the original by mistake" at the bottom of this guide before you commit anything.

Inside your own repository, working on `main` is fine. It is your copy, so you cannot break the original and nobody else's work can collide with yours.

---

## STEP 5: Do some work, then commit it

This is the loop you repeat for the whole project.

**See what changed:**
```
$ git status
```
Red files are changed but not staged. Green files are staged and ready to commit.

**Stage the files you want to commit:**
```
$ git add firmware/Core/Src/main.c
$ git add FIELD-LOG.md
```
Or stage everything that changed:
```
$ git add .
```

**Commit, with a message saying what you did:**
```
$ git commit -m "Read CO2 from the sensor over I2C"
```

Good messages say what changed. `fix stuff` is a commit message in the same sense that `it doesn't work` is a bug report.

**See your history:**
```
$ git log --oneline
```

---

## STEP 6: Push to your repository

Pushing uploads your commits to your repository on GitHub so we can see them.

```
$ git push
```

That is all it takes, every time, including the first. Cloning already linked your computer to your repository.

Push at the end of every session. We open your repository from GitHub, not from your laptop.

---

## STEP 7: Check it worked

Go to your repository on GitHub: `github.com/<YOUR-USERNAME>/<REPO>`. Your files and commits should be there. Send your Handler that link (and add us as a collaborator first if you made it private).

If they are not there, you have not pushed. Run `git status` and see what it says.

---

## The whole loop, once you are set up

```
$ git status                              # what changed?
$ git add .                               # stage it
$ git commit -m "what I did"              # save a snapshot
$ git push                                # upload it
```

Four commands. That is the job.

---

## When something goes wrong

**`fatal: not a git repository`**
You are in the wrong folder. `cd` into the cloned repository first.

**`Please tell me who you are`**
You skipped step 2. Run those two `git config` commands.

**`Updates were rejected because the remote contains work that you do not have`**
You pushed from another machine, or edited a file on the GitHub website. Run:
```
$ git pull
$ git push
```

**`remote: Permission denied`, or `error: failed to push some refs` with a 403**
**I cloned the original by mistake**
You are trying to push to the original repository, and you are not allowed to. That is deliberate. Create your own repository from the template first (step 3), then point your local copy at it:
```
$ git remote set-url origin https://github.com/<YOUR-USERNAME>/<REPO>.git
$ git push
```
Your commits are kept.


## References

- **Official git book**, free, genuinely good: https://git-scm.com/book/en/v2
- **GitHub quickstart:** https://docs.github.com/en/get-started/quickstart
- **Interactive branching visualiser**, 20 minutes well spent: https://learngitbranching.js.org/
- **Oh Shit, Git!?!** for fixing mistakes: https://ohshitgit.com/

---

## What we check

- You worked in your own repository, created from the template, and nothing was pushed to the original.
- At least 8 commits across at least 4 different days.
- `FIELD-LOG.md` committed alongside the code it describes, not written up at the end.
- Everything pushed to your repository before your debrief.

Commit your mistakes. A history with no bugs in it describes a project that did not happen.