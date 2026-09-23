# 00 — Get Lean running

[Course home](../README.md) · [First session](../START_HERE.md)

You will use three tools:

| Tool | Job |
| --- | --- |
| Lean | Checks definitions and proofs |
| Elan | Installs and selects Lean versions |
| Lake | Builds a Lean project and provides its environment |

VS Code's Lean extension gives you the interactive view of your proof. The official installation route is VS Code, the **Lean 4** extension, and its setup guide. Follow the [official installation page](https://lean-lang.org/install/) if its screens differ from these instructions.

## Install and open this project

1. Install [Visual Studio Code](https://code.visualstudio.com/) if needed.
2. Install the official [Lean 4 extension](https://marketplace.visualstudio.com/items?itemName=leanprover.lean4), identifier `leanprover.lean4`.
3. Follow the extension's setup guide to install its required tools. You can open the guide from the `∀` menu, then Documentation → Docs: Show Setup Guide.
4. Use **File → Open Folder** and choose this `formal_methods` folder. Open a `.lean` file so the extension activates.
5. Allow the project toolchain to download. The `lean-toolchain` file requests `leanprover/lean4:v4.23.0`.
6. Open a fresh integrated terminal after installation. From this folder, run:

```bash
lean --version
lake --version
lake build
bash scripts/check.sh examples
```

The Lean version should report `4.23.0`. The last command should end with `PASS: examples`. The printed `Nat`, `Prop`, and `9` come from demonstrations in the examples file; they are expected.

On this Mac, the project location is:

```bash
cd /Users/djsydney/Downloads/learning/formal_methods
```

If you move the folder, use its new location. Do not run `lake init`: this is already a project. Do not install Mathlib for this course. Your first Lean download can be several hundred megabytes and take a while.

## Meet the Infoview

Open [Course/Examples.lean](../Course/Examples.lean). Click inside the proof of `identity`. If the panel is hidden, use the Command Palette and search for **Lean Infoview**.

Move the cursor through these two lines:

```text
intro hP
exact hP
```

Around the first line, you should see the goal change from `P → P` to `P`, with `hP : P` available. After the proof is complete, there are no remaining goals. Cursor position affects which intermediate state is shown.

The editor helps you develop a proof. The terminal checks the saved file. Save before checking.

## Check your own work

```bash
bash scripts/check.sh 01
bash scripts/check.sh 02
bash scripts/check.sh 03
bash scripts/check.sh 04
bash scripts/check.sh 05
```

Use the number of the file you have finished. Each command also checks the shared teaching code. To check every exercise after the whole course:

```bash
bash scripts/check.sh all
```

For ordinary feedback that allows unfinished proofs:

```bash
lake env lean exercises/01_Warmup.lean
```

A successful command with a `sorry` warning **does not mean the exercise is proved**. The strict script uses `-DwarningAsError=true` to catch that distinction. It also rejects unrelated warnings, such as unused variables: read the message before assuming the logic is wrong.

## If something goes wrong

| Symptom | First thing to try |
| --- | --- |
| `lean` or `lake`: command not found | Reopen the terminal after Elan setup. If `~/.elan/env` exists, run `source "$HOME/.elan/env"`. |
| Wrong Lean version | Run from the folder containing `lean-toolchain`. Check `pwd`. |
| Missing `Course` or `.olean` file | Run `lake build` from the project root, then use `lake env lean`, not bare `lean`, for an exercise. |
| Editor has no goals | Open a `.lean` file, check that the Lean 4 extension is enabled, and show its Infoview. |
| Download failed | Read the extension's setup message; check connectivity and retry the setup. Do not change the pinned version as a first fix. |
| `declaration uses 'sorry'` | Finish the remaining proof holes in that file. |

The terminal instructions here target your Mac's shell. The editor setup also supports other platforms; Windows shell commands may need WSL or adaptation.

## Browser fallback

You can try a self-contained proof at [Lean's live editor](https://live.lean-lang.org/):

```lean
example (P : Prop) : P → P := by
  intro hP
  exact hP
```

The browser does not contain this project's `Course` module and may use a different Lean version. For a function exercise, copy the needed definition from `Course/Models.lean` and the exercise statement, omitting the project import. The local pinned project is the reproducible route for completing all checks.

Further detail: [Elan toolchains](https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/) and [Lake](https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/).
