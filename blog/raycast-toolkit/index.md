---
layout: post
title: "Introducing my Raycast Toolkit"
date: 2026-03-10
---

I am Nodoka, and I write for fun 🤓

I was introduced to Raycast by my friend Alan Huang from my internship with OMRON. Today I will delve into what it is and how you can set it up to optimize and customize a seamless workflow on your MacBook.

P.S. they released a Windows version in March, 2026  (and new version to come for macOS soon) 🎉

<details markdown="1"><summary>Updates</summary>

[2026.03.10] - Finished v1 + Published

</details>

## What even is Raycast?

> {% include card.html url="https://www.raycast.com/" %}
{: .callout .callout-link}

demo video by Raycast:

[https://youtu.be/NuIpZoQwuVY](https://youtu.be/NuIpZoQwuVY)

A lot of people describe Raycast as a “better Spotlight.” This is a misleading comparison, because the goal is different.

Raycast helps you execute actions directly from the keyboard. For example:

- access clipboard history
- run scripts or commands
- control windows

Normally you would open multiple applications or navigate menus to do these tasks. Raycast lets you to complete this in a single command.

As `/URDesign465` put it in a Reddit thread ([Spotlight beats Raycast?](https://www.reddit.com/r/raycastapp/comments/1ml3cji/spotlight_beats_raycast/)):

> Raycast is not really about Spotlight. It’s about closing the gap between plan and execution. Any friction in your workflow can be reduced or eliminated with Raycast.

## Installation

> Install Raycast from here:
>
> [Raycast - Your shortcut to everything](https://raycast.com/)
{: .callout}

I recommend changing the Raycast shortcut from `Alt + Space` to `Cmd + Space`.

Since `Cmd + Space` is used by Spotlight by default, you will first need to disable the Spotlight shortcut in System Settings.

After disabling it, set Raycast’s shortcut to `Cmd + Space`.

> ☝ I recommend you install [Arc from The Browser Company](https://arc.net/) for the full keyboard optimization experience´. I talked about this in my other blog ([my macos I](/blog/macos-setup-i/))
{: .callout}

## Setup basic tools first

Raycast has many cool built in tools! You can set the hotkey for each thing up by searching them up on `Extensions -> Hotkey` .

**#1. Emoji Picker by Raycast**

> [Emoji Extension for Mac \| Raycast](https://www.raycast.com/core-features/emoji-picker)
>
> I have `Alt + E` to show this.
{: .callout}

**#2. QuickLink by Raycast**

> [Quicklinks](https://manual.raycast.com/quicklinks)
>
> I have [`https://google.com/search?q={argument}`](https://google.com/search?q=%7Bargument%7D) that launches `Arc` . You could also have it launch ChatGPT via browser.
{: .callout}

Quicklinks is also a good way to manage and limit the number of tabs you have in your browser. Browsing via Quicklinks will open a new window in which you can choose to:

1. move to your main window (`Cmd + O` in Arc)
1. close window (universally, `Cmd + W` ).

**#3. Notes by Raycast**

> [Notes](https://manual.raycast.com/notes)
>
> I have `Alt + N` that opens Notes. I take some random thoughts / ideas on this. I like Raycast Notes rather than Apple Notes because It uses `markdown`
{: .callout}

**#4. Snippets by Raycast**

> [Snippets](https://manual.raycast.com/snippets)
>
> I have `!web` that pastes my website link and `!link` that pastes my LinkedIn link. I also have some common snippets of scripts and loops, as well as commonly used shell commands.
{: .callout}

**#5. Clipboard History**

> [Clipboard History for Mac \| Raycast](https://www.raycast.com/core-features/clipboard-history)
>
> I have `Cmd + Alt + V` to show me clipboard. It is technically *faster* to setup a shortcut for `Paste Sequentially` .
{: .callout}

**#6. Calculator by Raycast - No Additional Setup**

> [Calculator](https://manual.raycast.com/calculator)
>
> The calculator by Raycast is FIRE. It can convert currency, timezones and do complex calculations. I found this especially useful when I was in Japan, and had a meeting with my teams in the US.
{: .callout}

**#7. File Explorer by Raycast - No Additional Setup**

> [Mac File Explorer - Raycast File Search Extension \| Raycast](https://www.raycast.com/core-features/file-search)
>
> By launching Raycast and searching `Search Files` , Raycast will fuzzy search your files. By pressing on `Enter` , you can open the file.
{: .callout}

I started to use the File Explorer on Raycast extensively after I did factory reset on my Mac and reorganized my folders on Mac. This is because, now, I know the naming for all files locally saved on my computer.

On the side note, my workflow has improved since I started to organize my files as:

- 📁 assets/
   - jobs/resumes
      - bunch of resume versions
   - jobs/coverletter/
   - video-editting/
      - 20260213/{bunch of videos for material}
   - …
- 👩‍💻 dev/
   - my GitHub repos are cloned here.
- 🤖 research/
   - my presentation slides and Zotero (Google Drive) are here.

**(#8. Window Manager by Raycast)**

> [Window Management](https://manual.raycast.com/window-management)
>
> I do not use the window management by Raycast. As mentioned in my other blog ([my macos I](/blog/macos-setup-i/)), I use Rectangle because it allows for movement across desktops.
{: .callout}

Benefit of Raycast’s Window Management is its cycling behavior. This means that repeatedly pressing `Move to Right` (for me, this is `Ctrl + Alt + L`) cycles through layouts:

1. right half
1. left half
1. one-third column...

Some users prefer this approach for quickly switching between layouts.

## Extensions I use

Cool thing about the Raycast extensions is that they are all open sourced and contribution by the community. I do not use many, but I hope I can contribute to some (especially Notion one) soon when I am done with job search.

**#1. Kill Process**

> [Raycast Store: Kill Process](https://www.raycast.com/rolandleth/kill-process)
>
> I have `Alt + K` set to launch this. This is super useful for someone like me who uses 8GB RAM MacBook.
{: .callout}

**#2. GitHub**

> [Raycast Store: GitHub](https://www.raycast.com/raycast/github)
>
> I use this to create issues and PR in combination.
{: .callout}

**#3. Notion**

> [Raycast Store: Notion](https://www.raycast.com/notion/notion)
>
> I use this to open my databases with one command.
{: .callout}

This is especially useful because I keep pages for many different domains of my life. For example, I maintain a page called `Effective Coding`, where I collect useful references for writing code (ROS2 syntax, git commit conventions, etc.). With this extension, I can quickly jot down notes with a single command. Ultimately, my goal is to have an unified database of my brain on Notion (knowledge management).

P.S. I have tried using Obsidian. It did not me fit well 😟 I use Logseq for task management.

**#4. Spotify**

> [Raycast Store: Spotify Controls](https://www.raycast.com/thomas/spotify-controls)
>
> I have `Alt + L` and `Alt + H` for volume control, and `Ctrl + Shift + L` and `Ctrl + Shift + H` for skipping and going back to songs.
{: .callout}

> Again, I do not use many of the extensions but there is definitely more cool tools for you to explore!

## Upcoming releases…

[https://www.youtube.com/watch?v=Mi173xGb0ZA](https://www.youtube.com/watch?v=Mi173xGb0ZA)

I have always dreamt of building a `J.A.R.V.I.S`. I envision that Raycast with this update will be like J.A.R.V.I.S running locally on my macOS.

![After Raycast 2026 March update.](1.png)

They also released **`Glaze`****,** which is a vibe coder for Desktop applications. Easily deployed locally and launched to App Store for public usage. You can now join the Waitlist.

[https://www.youtube.com/watch?v=2s_NbPY_XuY](https://www.youtube.com/watch?v=2s_NbPY_XuY)

## Competitors

Does Raycast have competitors? Yes.

If there is one worth mentioning, it is built by **Mikker…** also known as the GOAT 🐐.

> {% include card.html url="https://tunaformac.com/" %}
>
> Visit Mikkel’s X to stay updated ([Mikkel Malmberg (@mikker) on X](https://x.com/mikker))
{: .callout}

This is really cool. I want to try the **breadcrumbs** feature in the future. For now, it still seems a bit too beta for me to spend time setting it up lol.

## Concluding Remarks

It’s hard to describe how powerful Raycast is with words. You really have to start using it, get past the small learning curve, and force yourself to use it instead of reaching for the mouse. The coolest part about Raycast, in my opinion, is that it is accessible and open, making it easy for people to contribute.

As AI becomes more embedded in how software is built, I think, the value of open collaboration becomes even more important. Tools improve when people share how they think and solve problems. Open projects allow ideas to circulate, evolve, and compound in ways closed systems rarely can.

As Vint Cerf (a.k.a. the founder of internet) once said:

> Information flow is what the Internet is about. Information sharing is power. If you don't share your ideas, smart people can't do anything about them.

> next blog = running [openclaw](https://github.com/openclaw/openclaw) 🦞
{: .callout}
