# Reviewer instructions — PromptLab T4 review

You've been asked to help review LLM outputs across the PromptLab cross-model panel. This page tells you how.

## What you're reviewing

For each of 24 prompts × 6 models = **144 cells** (plus 27 legacy cells from an earlier single-model run), you'll see:

- The original **source prompt** (what was sent to the model)
- The model's **raw output**
- A **machine-suggested triage** — a one-paragraph pre-draft from Claude Opus 4.7 to speed your read. It's labeled UNCONFIRMED and is intentionally conservative; it can flag obvious issues (fabricated citations, format violations, empty responses) but cannot judge domain correctness. **Read the raw output before trusting the triage.**

For each cell you set a verdict: **P** (Pass), **PN** (Pass with notes), **N** (Needs revision), or **?** (Cannot judge from output alone). You can also **Skip** cells you don't have expertise to review.

## Setup

1. **Use Chrome, Edge, or Opera** for the safest save mode (writes directly to a file on your disk every click).
   - Firefox and Safari work too, but fall back to browser storage — that's wiped if you clear cache. Stick with Chrome/Edge if you can.

2. **Open the review page:** `https://sharptonlab.github.io/PromptLab/docs/` *(once GitHub Pages is enabled by the PI)*

3. **Enter your name** — anything that uniquely identifies you (e.g. `tom-sharpton`). This is embedded in your verdicts file so attribution survives.

4. **Pick a verdicts file** when prompted. Two choices:
   - **Create a new file** (recommended for fresh review) — choose a memorable location like Desktop, name it e.g. `tom-sharpton-verdicts.json`.
   - **Open an existing file** if you're resuming previous work.

That's it. The header shows your save mode and reviewer name.

## Using the UI

- **Verdict buttons** (or keyboard: `P` / `B` / `N` / `Q` / `X`) set the verdict and auto-advance to the next ungraded cell.
- **Notes** field is for anything you want to record — saved on blur or `Cmd/Ctrl-S`.
- **Matrix panel** at top shows all cells color-coded by verdict. Click any cell to jump.
- **Prev / Next** navigate sequentially; **Shift + arrows** jump to prev/next ungraded.
- **Export backup** in the header downloads a snapshot any time — useful as belt-and-suspenders backup or for moving between machines.

## What to look for

The machine triage tells you what it could and couldn't check. Your job is the things it couldn't:

- **Domain correctness** — does the code actually compute the right statistic for the biological question? Does the recommended approach fit the data?
- **Citation truth** — does the cited paper actually say what's claimed?
- **Subtle distortions** — has the model preserved the intent of the input, or shifted emphasis / introduced unsupported claims?
- **Output usability** — would a real researcher get value from this response, or does it need significant rework?

If you're not sure on domain specifics, use `?` rather than guessing.

## Sending your verdicts back

When you're done (or want to send progress), you have two options. Pick whichever's easier:

### Option A — Email the file

1. Click **Export backup** in the page header. Downloads `<your-name>-verdicts.json`.
2. Email the file to the PI.

### Option B — Open a pull request

1. Click **Export backup** to download `<your-name>-verdicts.json`.
2. Go to the [repo on GitHub](https://github.com/SharptonLab/PromptLab) → click `verdicts/` directory → **Add file** → **Upload files**.
3. Drag in your file. GitHub auto-prompts to fork if you don't have write access — that's fine, click through.
4. Add a commit message like "Tom's T4 verdicts" → **Propose changes** → **Create pull request**.
5. A GitHub Action runs automatically and posts an inter-reviewer agreement report as a comment on your PR.

The PR option preserves a clean attribution chain and produces inter-rater agreement data the paper can cite. Use it if you're comfortable with GitHub.

## Safety notes

- **Your work is saved on every click** (to your local file in Chrome/Edge mode; to browser storage otherwise).
- Nothing is uploaded anywhere automatically — the file stays on your computer until you choose to share it.
- The page can be closed and reopened — pick the same verdicts file on reopen to resume.
- If the page tells you a save failed, click **Export backup** immediately to grab a snapshot.

## Questions

Email the PI (Tom Sharpton, thomas.sharpton@oregonstate.edu) or open an issue on the repo. The page itself prints any errors prominently — quote the error text in your message and we can debug.
