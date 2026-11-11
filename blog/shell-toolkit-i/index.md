---
layout: post
title: "Introducing my Shell Toolkit I"
date: 2026-04-29
---

this post introduces my current shell tool stack. it was originally part of my [my macos I](/blog/macos-setup-i/) blog, but that write-up became too long, so i moved the shell tooling into its own post.

in the process, i lost the original draft from the [my macos I](/blog/macos-setup-i/). that is probably for the better… the tools i listed then were not particularly strong (and i may feel the same about this list in a few months). for now, i’m calling this *my shell toolkit i*, leaving room for a future *ii*.

side note: i’ve finished my last exam this morning. this is my leisure time!

<details markdown="1"><summary>TL;DR I use these shell tools:</summary>

- [Git](https://git-scm.com/about#free-and-open-source)
- [Introduction · Tig - Text-mode interface for Git](https://jonas.github.io/tig/)
- [vim-fugitive](https://github.com/tpope/vim-fugitive)
- [lazygit](https://github.com/jesseduffield/lazygit)
- [fd](https://github.com/sharkdp/fd)
- [tmux](https://github.com/tmux/tmux)
- [sshs](https://github.com/quantumsheep/sshs)
- [htop - an interactive process viewer](https://htop.dev/)
- [zoxide](https://github.com/ajeetdsouza/zoxide)
- [fzf](https://github.com/junegunn/fzf)
- [rsync](https://github.com/RsyncProject/rsync)
- [rclone](https://github.com/rclone/rclone)
- [dua-cli](https://github.com/Byron/dua-cli)
- [baobab](https://github.com/GNOME/baobab)
- [hyperfine](https://github.com/sharkdp/hyperfine)
- [pueue](https://github.com/Nukesor/pueue)
- [ripgrep](https://github.com/burntsushi/ripgrep)

</details>

<details markdown="1"><summary>Updates</summary>

[04/29/2026] - v1 published🎉

</details>

## neovim

> {% include card.html url="https://github.com/neovim/neovim" %}
{: .callout .callout-link}

i talked about this already in [my macos I](/blog/macos-setup-i/) blog, but `neovim` is where this whole shell obsession started. once i was living inside a terminal editor, everything else followed. i wanted the tools around it to match that speed and keyboard-first feel.

neovim is also what ties most of this stack together. [ripgrep](https://github.com/burntsushi/ripgrep) as the grep backend, [fzf](https://github.com/junegunn/fzf) for fuzzy finding, [vim-fugitive](https://github.com/tpope/vim-fugitive) for git. they're all plugins or integrations that live inside neovim. so it belongs at the top.

if you haven't read the macos post, the short version: neovim is an improved vim where you write your config in `.lua`. start with [kickstart.nvim](https://github.com/nvim-lua/kickstart.nvim) if you want to give it a try.

## git

> {% include card.html url="https://github.com/git/git" %}
{: .callout .callout-link}

for obvious reasons, you need git. it tracks and manages changes in your code. technically, a "distributed version control system." note that git is not github. git is THE version control system. GitHub is just a web-based host for your git repos.

one thing i will say: **just learn git**. GUIs like [GitKraken](https://github.com/gitkraken) add a layer that makes version control slower and less capable, not easier. there was a whole reddit thread about GitKraken going paid and i think `[deleted]`'s response summed it up well. your product is built on top of git, which is free. learn the thing itself.

i use [commitlint](https://github.com/conventional-changelog/commitlint) on git to maintain good commit comments. highly recommend that you use this.

## tig

> {% include card.html url="https://github.com/jonas/tig" %}
{: .callout .callout-link}

have you ever:

```shell
git log --all --graph --oneline --decorate \
  --pretty=format:'%C(auto)%h %d %s %C(black)%C(bold)%cr'
```

i have. and then tig changed my life. now i just run

```shell
tig --all
```

and it is so pretty. you get a colored, navigable graph of your entire commit history right in the terminal. you can browse commits, diff changes, inspect branches — all with vim-style keybindings. never going back.

## vim-fugitive

> {% include card.html url="https://github.com/tpope/vim-fugitive" %}
{: .callout .callout-link}

vim-fugitive is a git wrapper for neovim. the killer feature for me is `:G` (or `:Git`), which opens a staging window right inside neovim. you can stage individual hunks with `s`, unstage with `u`, and commit without ever touching the terminal.

from inside neovim:

```shell
# inside neovim
:G                  # open fugitive status window
s                   # stage a file (or hunk with =  to expand, then s)
cc                  # open commit message buffer
:wq                 # write and close -> commit done
:G push             # push without leaving neovim
```

it also means `gd` in the diff view, which i already love for code navigation, now works on git diffs too. everything stays in one place.

## fd

> {% include card.html url="https://github.com/sharkdp/fd" %}
{: .callout .callout-link}

`fd` is a replacement for `find`. i find `find` is annoying to use.

```shell
# find
find . -name "*.py" -not -path "*/node_modules/*"

# fd
fd -e py
```

fd is faster, respects `.gitignore` by default, and the output is color-coded. there is no world where i am typing out a full `find` command when `fd` exists.

## tmux

> {% include card.html url="https://github.com/tmux/tmux" %}
{: .callout .callout-link}

i learned why i needed tmux the hard way.

i was SSH'd into a remote workstation running a training job. my connection dropped. the process died. the job was gone. i had to start over.

`tmux` is a terminal multiplexer. it runs sessions that persist even when you disconnect. so now when i SSH into a machine, the first thing i do is attach to a tmux session (or create one). if my connection drops, the job keeps running. i come back, reattach, and everything is exactly where i left it.

the other thing tmux gives you is panes and windows. you can split your terminal and have your training script, logs, and `htop` all visible at the same time without opening new terminal tabs. especially useful on a remote machine where you do not have a GUI.

my most used shortcuts:

- `Ctrl + b` then `"` : split horizontally
- `Ctrl + b` then `%` : split vertically
- `Ctrl + b` then `d` : detach (session keeps running)
- `tmux attach` : come back to it

## sshs

> {% include card.html url="https://github.com/quantumsheep/sshs" %}
{: .callout .callout-link}

i had an `~/.ssh/config` file. it worked. but remembering which alias mapped to which machine, especially when i'm managing a few different servers, was friction i did not need.

sshs reads your existing `~/.ssh/config` and gives you a fuzzy-searchable TUI to pick which host to connect to. no new config, no setup. just run `sshs`, search for the machine you want, and connect.

small tool, but i use it every day.

## htop

> {% include card.html url="https://github.com/htop-dev/htop" %}
{: .callout .callout-link}

htop is an interactive process viewer. you probably know `top` but, htop is just better. color-coded CPU and memory bars, scrollable process list, and you can kill or renice processes directly from the interface.

i've tried `btop` and `nvtop`. they look nice. but `htop` gives me exactly the information i need without extra visual noise, and it's available on basically every machine i SSH into without having to install anything.

i usually have it open in a tmux pane alongside whatever job is running. so i can see CPU and memory usage in real time without context switching.

## rsync

> {% include card.html url="https://github.com/RsyncProject/rsync" %}
{: .callout .callout-link}

have you ever tried to copy a file that so large it takes 10 hours to copy? i have!

have you ever had your computer crash on you mid way and your `cp` ed files are never found? yes!

well, no more crashouts because now you can `rsync` your files. you can pause the sync and files will never be deleted. if the transfer gets interrupted, you just run it again and it picks up where it left off. it only transfers what changed, so there is no wasted time re-copying files that already made it over.

## rclone

> {% include card.html url="https://github.com/rclone/rclone" %}
{: .callout .callout-link}

`rclone` is rsync, but for cloud storage. i use it to sync data to and from AWS S3. the interface is almost identical to rsync, which made it easy to pick up.

```shell
rclone sync ./local-data s3:my-bucket/data --progress
```

useful when you have model checkpoints or datasets sitting on a remote server that you want backed up to S3, or when you need to pull data down to a new machine without going through a browser.

## dua-cli

> {% include card.html url="https://github.com/byron/dua-cli" %}
{: .callout .callout-link}

[baobab](https://github.com/Yomguithereal/baobab)

dua-cli (`dua i`) is a fast interactive TUI for seeing what's taking up disk space. it's like `du` but you can actually navigate it. you go directory by directory and delete things right from the interface.

baobab is the GUI equivalent. it is more visual, better for when you want a bird's eye view of your storage as a tree diagram. i use `dua` on remote machines and `baobab` locally when i want to see the big picture.

## zoxide

> {% include card.html url="https://github.com/ajeetdsouza/zoxide" %}
{: .callout .callout-link}

i got tired of typing `cd ../../some/deeply/nested/folder` every time i wanted to go somewhere i had already been. zoxide tracks the directories you visit and lets you jump to them by typing a fraction of the name.

```shell
# instead of
cd /Desktop/dev/project

# just
z project
```

and because i'm usually going to the same handful of places, `z dev` gets me there instantly. the other thing i use constantly is `zi`. it opens a fuzzy finder of your most visited directories so you can interactively pick where to go.

```shell
zi foo   # shows all dirs matching "foo", navigate with arrow keys
```

one of those tools where you install it and wonder how you lived without it.

## pueue

> {% include card.html url="https://github.com/Nukesor/pueue" %}
{: .callout .callout-link}

when i want to test several model configs overnight, i can't just run them all in parallel. i don't have enough compute for that. i used to run one job, wait for it to finish, come back, start the next one. that got old fast.

pueue is a task queue manager for the terminal. you add jobs to the queue and it runs them one after another (or in parallel up to a limit you set). each job's output is logged. you can pause, reorder, or kill jobs.

```shell
pueue add -- python train.py --config config_a.yaml
pueue add -- python train.py --config config_b.yaml
pueue add -- python train.py --config config_c.yaml
```

now i queue everything up before i go to sleep and check results in the morning. it is a small workflow change that saves a lot of babysitting.

## ripgrep

> {% include card.html url="https://github.com/burntsushi/ripgrep" %}
{: .callout .callout-link}

ripgrep (`rg`) is a line-oriented search tool. it's faster than `grep`, respects `.gitignore`, and the output is color-coded by default.

i use it in two places. in the terminal when i want to search a codebase for a string or pattern quickly. and inside neovim through telescope, where it powers live grep across the entire project.

```shell
rg "forward_pass" --type py
```

once you have ripgrep as your neovim grep backend, searching your project feels instant. i would not go back to `grep` for this.

## neovim

> {% include card.html url="https://github.com/neovim/neovim" %}
{: .callout .callout-link}

neovim actually changed my life. neovim is improved version of vim that allows you to write the config in `.lua` . if you are in the software space, you should learn neovim. at least vim. however, i must say that because i use VSCode neovim, i end up using basic vim. i am moving onto neovim editor based coding outside of ides.

you can setup neovim with [kickstart.nvim](https://github.com/nvim-lua/kickstart.nvim). in which you need to install these followings:

[fzf](https://github.com/junegunn/fzf)

[tree-sitter](https://github.com/tree-sitter/tree-sitter)

[lua](https://github.com/lua/lua)

## hyperfine

> {% include card.html url="https://github.com/sharkdp/hyperfine" %}
{: .callout .callout-link}

hyperfine is a command-line benchmarking tool. you give it a command (or two), it runs them many times, and gives you mean, standard deviation, and a comparison if you pass multiple.

i use it when i want to know if one version of a script is actually faster than another, rather than guessing.

```shell
# benchmark a single script
hyperfine 'python preprocess.py'

# compare two versions
hyperfine 'python preprocess_v1.py' 'python preprocess_v2.py'
```

the output tells you which is faster and by how much, with confidence. much better than running `time` manually a few times and eyeballing it.

## Conclusion

this stack will probably look different in six months. every tool here came from noticing some friction, asking if there was a better way, and usually finding that someone had already built it.

if you find something i should try, let me know.
