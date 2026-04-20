# Lab 8 Step-by-Step Guide

This guide is tailored to your current workspace at `C:\AI4SE`.

Important note:
- I did **not** find any Lab 8 PDF inside `C:\AI4SE`.
- So this guide is based on:
  - your local repos
  - Denis' email
  - the Teams message
- If you add the PDFs into `C:\AI4SE`, the guide can be refined line-by-line against them.

## What I found in your workspace

- `C:\AI4SE` is a workspace folder, **not** a git repo itself.
- Your labs are separate repos inside it.
- `C:\AI4SE\lab1-hello-world` exists and contains:
  - `.github\copilot-instructions.md`
  - `.github\agents\journal-logger.agent.md`
- `C:\AI4SE\lab1-hello-world` points to the class repo:
  - `https://github.com/bcs-s2-2026/lab1-hello-world.git`
- `C:\AI4SE\lab7-bubble-sort` already points to your GitHub repo:
  - `https://github.com/iradukunda277/lab7-bubble-sort.git`
- I did **not** find a `lab8` folder yet in `C:\AI4SE`.
- I did **not** find any `.pdf` file in `C:\AI4SE`.

## What Denis is asking you to do

From the screenshots, the expectations are:

1. Use the **latest** `.github` folder from `lab1-hello-world` before starting Lab 8.
2. Create and work in a **separate Lab 8 repo**.
3. Send Denis the **link to your Lab 8 repo** at least once.
4. Do as much coding as possible **yourself**.
5. Use **Socratic mode**, **stubs**, and **TODOs**.
6. Keep the features from the previous lab, including the **small rotation-speed update** to the square.
7. Understand your own code well enough to work on it live.

## Recommended repo name

Use:

`lab8-pygame`

That matches Denis' wording and keeps your repo names consistent.

## Step-by-step workflow

### 1. Update your class starter repo first

Open PowerShell and run:

```powershell
cd C:\AI4SE\lab1-hello-world
git remote -v
git pull origin main
```

Expected remote:

```text
https://github.com/bcs-s2-2026/lab1-hello-world.git
```

If Git shows a `dubious ownership` error, run:

```powershell
git config --global --add safe.directory C:/AI4SE/lab1-hello-world
```

Then retry:

```powershell
git pull origin main
```

### 2. Create the Lab 8 repository on GitHub

In GitHub:

1. Click `New`.
2. Repository name: `lab8-pygame`
3. Keep it under your account: `iradukunda277`
4. Create the repo

Do not create Lab 8 inside `lab7-bubble-sort`. It should be its own repo in `C:\AI4SE`.

### 3. Clone the new Lab 8 repo into your workspace

```powershell
cd C:\AI4SE
git clone https://github.com/iradukunda277/lab8-pygame.git
cd C:\AI4SE\lab8-pygame
```

If Git gives the same ownership warning later, run:

```powershell
git config --global --add safe.directory C:/AI4SE/lab8-pygame
```

### 4. Copy the required course scaffolding from `lab1-hello-world`

This is the most important instruction from Denis.

Run:

```powershell
Copy-Item -Recurse C:\AI4SE\lab1-hello-world\.github C:\AI4SE\lab8-pygame\
Copy-Item C:\AI4SE\lab1-hello-world\.gitignore C:\AI4SE\lab8-pygame\.gitignore
Copy-Item C:\AI4SE\lab1-hello-world\REPORT.md C:\AI4SE\lab8-pygame\REPORT.md
New-Item -ItemType File C:\AI4SE\lab8-pygame\JOURNAL.md
```

Why this matters:
- `.github` gives you the AI instructions Denis wants
- Socratic mode is enabled by default there
- the journal/logger workflow matches the course setup
- `REPORT.md` gives you the expected reflection structure

### 5. Create the basic Lab 8 file structure

At minimum, create:

```text
lab8-pygame/
├── .github/
├── JOURNAL.md
├── REPORT.md
├── README.md
├── main.py
└── test_main.py
```

If your project uses assets, also add:

```text
assets/
```

### 6. Set up Python and install dependencies

Inside `C:\AI4SE\lab8-pygame`:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pygame pytest
```

Optional:

```powershell
pip freeze > requirements.txt
```

### 7. Turn the lab requirements into a checklist before coding

Since the PDFs are not in this workspace yet, make a checklist from:
- the Lab 8 PDF
- Denis' email
- the Teams post

Your checklist should include two groups:

Confirmed from Denis:
- latest `.github` copied from `lab1-hello-world`
- Lab 8 repo created and pushed
- repo link sent to Denis
- Socratic mode / stubs / TODOs used
- previous lab features preserved
- small rotation-speed update included

From the Lab 8 PDF:
- add every feature requirement as a checkbox
- add controls the user must support
- add deliverables like README, report, screenshots, tests, or demo notes if required

### 8. Start with stubs and TODOs

Because Denis explicitly asked for stubs and TODOs, start simple.

Example structure for `main.py`:

```python
def handle_input():
    # TODO: handle keyboard input
    pass

def update_game_state():
    # TODO: update movement / rotation / speed
    pass

def draw_scene():
    # TODO: draw square and UI
    pass

def main():
    # TODO: initialize pygame and main loop
    pass

if __name__ == "__main__":
    main()
```

This keeps the code understandable and easy to explain live.

### 9. Implement in small, testable steps

Recommended order:

1. Open a Pygame window successfully.
2. Draw the square.
3. Add movement/update logic.
4. Add rotation logic.
5. Add the small rotation-speed update Denis mentioned.
6. Add keyboard controls.
7. Add any extra Lab 8 PDF features.
8. Clean up the code and comments.

After each small step:

```powershell
python main.py
```

If you have unit-testable logic, also run:

```powershell
pytest
```

### 10. Write the README as you go

Your `README.md` should explain:
- what the project does
- how to install dependencies
- how to run it
- what the controls are
- what features are implemented

Use your `lab7-bubble-sort` README as a quality reference for structure.

### 11. Update `REPORT.md` honestly

Do not leave the report empty.

Make sure you write about:
- what you understood at the start
- what you learned
- where AI helped
- where AI was wrong or unhelpful
- when you trusted AI and when you checked it
- how Socratic mode changed your workflow

### 12. Commit and push early

Do not wait until the very end.

Suggested first commit:

```powershell
git add .
git commit -m "chore: scaffold lab8 pygame project"
git push -u origin main
```

Then keep using small commits, for example:

```powershell
git add .
git commit -m "feat: add pygame window and square rendering"
git push
```

### 13. Send the repo link to Denis

This is required based on the Teams message.

After your first push, send:

`https://github.com/iradukunda277/lab8-pygame`

Even if the project is not finished yet, Denis said the repo link had to be sent at least once.

### 14. Prepare for the live check

Before Monday, be ready to explain:

1. How your main loop works
2. How input is handled
3. How square movement and rotation work
4. How the speed update works
5. What AI helped with
6. What code you personally understand and can modify

## Definition of done

You are in a good position when all of these are true:

- `lab8-pygame` exists in `C:\AI4SE`
- the repo exists on GitHub
- `.github` was copied from updated `lab1-hello-world`
- `main.py` runs
- the required controls/features work
- the small rotation-speed update works
- `README.md` is filled in
- `REPORT.md` is filled in
- `JOURNAL.md` exists and is being used
- your repo has been pushed
- Denis has received the repo link

## Most likely blocker right now

The main blocker is not code yet. It is missing task text.

I still need the Lab 8 PDF to convert this into an exact requirement-by-requirement plan.

## Best next action

Do these three things first:

1. Pull the latest `lab1-hello-world`
2. Create `lab8-pygame` on GitHub and clone it into `C:\AI4SE`
3. Put the Lab 8 PDF into `C:\AI4SE` so the checklist can be made exact
