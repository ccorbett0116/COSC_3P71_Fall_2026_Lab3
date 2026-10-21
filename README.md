# Lab 3: Seeing with the Camera

In Lab 2 the robot's whole view of the world was **4 bits**: four line sensors
saying "black" or "not black". In Lab 3 you give it a camera. One camera frame
is about **300,000 pixels**, each with three colour values. That's far more
information, and far more work to turn into something an agent can act on.

By the end of this lab, your robot can look at objects and say what they are:

```
   ┌──────────────────────────────────────────────┐
   │  red cube, blue sphere, yellow cube           │
   │                                              │
   │      ┌──────┐            ╭────╮               │
   │      │ red  │           ( blue )   ┌─────┐    │
   │      │ cube │            ╰────╯    │yellow│   │
   │      └──────┘          sphere      └─────┘    │
   └──────────────────────────────────────────────┘
```

This is **perception**, the "sense" step of the agent loop from Lab 2, done the
hard way: from raw pixels.

> **This lab is deliberately hands-off.** You get this README, an almost empty
> `vision.py` and a self-check, nothing else. You write all the code. You'll also
> go back into your **own Lab 2 code** and extend it. Expect to read
> documentation, search, experiment and get things wrong before they work. That
> *is* the lab.

---

## ⚠ Read this first: use AI tools BEFORE you ask your TA

For this lab you are **expected** to use AI assistants (ChatGPT, Claude, Copilot,
Gemini, ...) and documentation as your **first** source of help. Your TA is your
**second** stop, not your first.

**The rule:** before you ask a TA a question, you must have tried to answer it
yourself with an AI tool and/or the documentation. When you ask, **show your TA
what you tried**:

1. what you asked the AI tool (the actual prompt, or the chat itself),
2. what it told you,
3. what you tried because of that, and what happened (error message, `--check`
   output, screenshot, ...).

A TA can and will send you back with *"what did the AI say when you asked it?"*
if you haven't done this. Keep your chats open or save the links, so you can
show them.

**How to use AI tools well in this lab:**

- **Ask it to explain, not just to write.** "What does `cv2.inRange` do and why
  do people convert to HSV first?" teaches you more than "write me a colour
  detector".
- **Paste the full error message** (or the `FAIL:` line from `--check`) and the
  code around it. "It doesn't work" gets you a useless answer.
- **Describe what you see.** "My mask is all white except for the ball" is
  something an AI tool can reason about.
- **Check what it tells you.** AI tools are confidently wrong sometimes: they
  invent function arguments, mix up OpenCV versions and forget that OpenCV hue
  only goes to 179. Run it, look at the result, and ask again if it's wrong.
- **You must understand every line you hand in.** At your demo the TA will
  point at lines in your `vision.py` and ask you to explain them. "The AI wrote
  it" is not an explanation. If you can't explain a line, ask the AI to explain
  it to you until you can, or rewrite it.

---

## Quick reference

Run everything from **your Lab 2 folder** (the one with `run_robot.py`):

```bash
python vision.py --check     # test your work. No robot or camera needed. Run it often.
python vision.py             # your vision program, on the robot's camera
python run_robot.py          # your Lab 2 window, with the Open Camera button
```

---

## What you'll do

| Stage | What | Where |
|---|---|---|
| **Setup** | Get this repo, copy three files into your **Lab 2** folder (replacing `requirements.txt`), install the packages | your `Lab_2/` folder |
| **Stage 1** | Add an **Open Camera** button to your Lab 2 GUI that starts `vision.py` | `turbopi/gui.py` (your Lab 2 code) |
| **Stage 2** | Write the computer vision: camera → colours → shapes → labels | `vision.py` |

You'll keep working **inside your Lab 2 folder**. Lab 3 adds to the program you
already have; it doesn't replace it.

`--check` tests every part of this lab on **pictures it draws itself**, so you can
build and test almost everything before you go near the robot. Each step below
says which `--check` line it turns to `ok`.

---

## Contents

1. [Setup](#1-setup)
2. [Stage 1: the Open Camera button](#2-stage-1-the-open-camera-button)
3. [Stage 2: computer vision in vision.py](#3-stage-2-computer-vision-in-visionpy)
   - [Step 1: show the camera](#step-1-show-the-camera)
   - [Step 2: find one colour](#step-2-find-one-colour)
   - [Step 3: clean up the mask](#step-3-clean-up-the-mask)
   - [Step 4: cube or sphere?](#step-4-cube-or-sphere)
   - [Step 5: every colour, every object, labelled](#step-5-every-colour-every-object-labelled)
   - [Step 6: run it on the robot](#step-6-run-it-on-the-robot)
4. [Troubleshooting](#4-troubleshooting)
5. [Demo checklist](#5-demo-checklist)

---

## 1. Setup

### 1.1 Get this repo

```bash
git clone <this repository's URL>
```

(Or download the ZIP from GitHub and unzip it.) It contains this README,
a skeleton `vision.py`, the self-check `lab3_check.py`, and a new
`requirements.txt`.

### 1.2 Move into your Lab 2 folder

Find **your own** Lab 2 folder, the one with **your** `line_follower.py` and
**your** finished Task 1 button in `turbopi/gui.py`. Run
`python run_robot.py --check` there once, to make sure your Lab 2 work still
passes before you change anything.

Then copy **three files** from this repo into it, **next to `run_robot.py`**:

```
Lab_2/
├── run_robot.py
├── line_follower.py      ← yours, from Lab 2
├── vision.py             ← copy it here (you'll write this)
├── lab3_check.py         ← copy it here (don't edit it)
├── requirements.txt      ← REPLACE it with the Lab 3 one
└── turbopi/
    └── gui.py            ← you'll edit this in Stage 1
```

⚠ **`requirements.txt` replaces your Lab 2 one.** When your computer asks whether
to replace the existing file, say **yes**. The new file lists everything Lab 2
needed **plus** OpenCV and NumPy for Lab 3, so nothing is lost.

From now on, **run every command from inside your `Lab_2` folder**, exactly as in
Lab 2.

### 1.3 Install the packages

```bash
pip install -r requirements.txt
```

This installs OpenCV (`opencv-python`) and NumPy, and checks the Lab 2 packages
are still there. If you ever set this project up on another computer, this one
command installs everything it needs.

### 1.4 Run the self-check

```bash
python vision.py --check
```

You should see:

```
Lab 3 self-check (no robot needed)

Setup    requirements.txt replaced with Lab 3's             ok
Stage 1  Open Camera button starts vision.py                not done yet
Step 1   open_source() opens an image file                  not done yet
Step 2   build_mask() finds each colour, nothing else       not done yet
Step 3   build_mask() removes specks and fills holes        not done yet
Step 4   classify_shape() tells cubes from spheres          not done yet
Step 5   detect() finds and labels every object             not done yet
Step 5   draw_detections() draws on the frame               not done yet
```

As you finish each part it changes to `ok`. If something is wrong, it prints a
`FAIL:` line saying what it expected and what your code did. **That `FAIL:` line
is the first thing to paste into an AI tool when you're stuck.**

`--check` calls the functions in `vision.py` **by name**: `open_source`,
`build_mask`, `classify_shape`, `detect`, `draw_detections` and the `COLOURS`
list. Keep those names and do what their docstrings say. Add as many other
functions as you like.

### 1.5 Check the robot's camera

When you're at the robot: turn it on, join its Wi-Fi (as in Labs 1 and 2) and
open this address in a **web browser**:

```
http://192.168.149.1:8080/stream?topic=/image_raw
```

You should see the live camera. If you do, OpenCV can open the same URL. If you
don't, sort that out with your TA before going further: it isn't a code problem.

---

## 2. Stage 1: the Open Camera button

**Goal:** a button in your Lab 2 window that starts your camera program.

You did almost exactly this in **Lab 2, Task 1**: you added the Line Follow
button to `turbopi/gui.py`. **Go back to your Lab 2 work and the Lab 2 README
(Task 1) and use them.** There are deliberately no step-by-step instructions
here.

**Requirements:**

- A button labelled **Open Camera** in the main window (put it wherever it makes
  sense, near the camera pad, say).
- Clicking it runs **`vision.py`** (the file next to `run_robot.py`).
- **While the camera program is open, the main window must keep working**: you
  can still drive, aim the camera with the camera pad and press STOP.
- If `vision.py` is missing, show a message in the window instead of crashing
  (Lab 2 did this for `line_follower.py`; find how).

**One hint, and a question to think about.** In Lab 2 the GUI *imported*
`line_follower.py` and called `step()` 10 times a second. The camera code is
different: it will run its own endless loop (grab a frame, process it, show it,
repeat). What would happen to the GUI, and to `publish_loop()`, the 10 Hz
`/cmd_vel` heartbeat, if you called that loop straight from your button?

The simplest way around this is to run `vision.py` as a **separate program**, the
same as typing `python vision.py` in a terminal, but started from Python. Look up
Python's `subprocess` module. Some of its functions wait for the program to
finish and some don't: which do you need? And why is `sys.executable` better than
just `"python"`?

> **Checkpoint:** `--check` says `Stage 1 ... ok`. It clicks your button
> *without really starting anything* and tells you if your button would freeze the
> GUI. Then run `python run_robot.py` and click it for real: the terminal shows
> *"vision.py is running - nothing implemented yet"*, and the joystick still works.

---

## 3. Stage 2: computer vision in vision.py

**Goal:** `vision.py` opens the camera and labels every cube and sphere it sees,
in red, green, blue and yellow.

Do the steps **in order**, and **run `--check` after each one**: a bug in Step 2
makes Step 4 impossible to get right.

Every step names the OpenCV functions you'll need. **Look each one up** in the
[OpenCV Python docs](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) or
ask an AI tool to explain it *before* you use it.

---

### Step 1: show the camera

**Goal:** a window showing the live camera. `q` closes it.

**You'll need:** `cv2.VideoCapture`, `.read()`, `cv2.imshow`, `cv2.waitKey`,
`cv2.destroyAllWindows`, `cv2.imwrite`, `sys.argv`.

1. Write **`open_source(source)`**. It takes the program's first argument and
   returns something you can call `.read()` on to get frames:

   | Command | `source` | Opens |
   |---|---|---|
   | `python vision.py` | `"robot"` | the robot: `STREAM_URL` |
   | `python vision.py 0` | `"0"` | webcam number 0 on this computer |
   | `python vision.py test.jpg` | `"test.jpg"` | a picture or video file |

   (`cv2.VideoCapture` can open all three. What type does it need for a webcam
   number?)
2. Write the loop in **`main()`**: read a frame, show it, repeat, until `q`.
3. Pressing **`p`** saves the current frame (the **raw** frame, with nothing drawn
   on it) into a `pictures/` folder. Take some pictures of each object with the
   robot's camera: you can test with them at home.

**Things to know:**

- OpenCV stores pixels as **B, G, R**, not R, G, B.
- `cv2.imshow` doesn't actually draw anything until `cv2.waitKey` is called.
  No `waitKey` in your loop means a grey, frozen window.
- `.read()` returns **two** things. What's the first one for, and what happens if
  you ignore it?
- A picture file gives you **one** frame, then `.read()` says it's finished.
  Make your loop cope (keep showing the last frame?), so you can test on a picture.

> **Checkpoint:** `--check` says `Step 1 ... ok`. A webcam or the robot shows up
> live in a window, `p` saves a picture and `q` quits. Your Stage 1 button opens it.

---

### Step 2: find one colour

**Goal:** a second window showing a **mask**: white where the picture is red,
black everywhere else.

**You'll need:** `cv2.cvtColor` (with `cv2.COLOR_BGR2HSV`), `cv2.inRange`,
`cv2.bitwise_or`.

**Why HSV and not BGR?** In BGR, a red ball's shadowed side and its lit side
have very different numbers. HSV separates *what colour* (**H**ue) from *how
strong* (**S**aturation) and *how bright* (**V**alue), so "red" becomes "hue near
0" no matter how it's lit. Ask an AI tool to explain HSV until you could draw the
picture yourself.

1. Fill in **`COLOURS`**: one dictionary per colour, each with a `"name"`
   (`"red"`, `"green"`, `"blue"`, `"yellow"`) plus whatever **you** need to
   describe it, such as an HSV range and a colour to draw with. Start with red.
2. Write **`build_mask(hsv, colour)`**: given a picture in HSV and one entry of
   `COLOURS`, return the mask.
3. Show the mask in its own window in `main()`.

**OpenCV-specific traps:**

- OpenCV hue runs **0 to 179**, not 0 to 360. S and V run 0 to 255. Most
  colour-picker websites and many AI answers use 0 to 360. Convert!
- **Red sits at both ends of the hue range** (around 170 to 179 *and* 0 to 10).
  One `inRange` call can't cover it. How do you combine two masks?

**Tune it, don't guess it.** Add trackbars (`cv2.createTrackbar`,
`cv2.getTrackbarPos`) for H min/max, S min/max and V min/max, and slide them until
only the object is white. Write the numbers down and put them in `COLOURS`.

> **Checkpoint:** `--check` says `Step 2 ... ok` once all four colours are in
> `COLOURS`. It tests your ranges on clean, bright test colours and on grey,
> white and black, which should never match. (`Step 3` may still fail: that's
> next.)

---

### Step 3: clean up the mask

**Goal:** a clean mask: no specks, no holes.

**You'll need:** `cv2.GaussianBlur`, `cv2.morphologyEx` (`MORPH_OPEN`,
`MORPH_CLOSE`), `cv2.getStructuringElement`.

Real masks are noisy: speckles of "red" in the background, holes in the object.

1. **Blur** the frame a little before converting it to HSV (in `main()` or
   `detect()`: think about where).
2. Inside `build_mask()`, **open** the mask (removes specks) and then **close** it
   (fills holes). Look up what each one does to a picture: it's worth
   understanding.

> **Checkpoint:** `--check` says `Step 3 ... ok`. In your mask window, the object
> is solid white and the background is black.

---

### Step 4: cube or sphere?

**Goal:** **`classify_shape(contour)`** returns `"cube"`, `"sphere"` or
`"unknown"` for one outline.

**You'll need:** `cv2.findContours`, `cv2.contourArea`, `cv2.arcLength`,
`cv2.approxPolyDP`, `cv2.drawContours`, `cv2.putText`.

First, turn the mask into outlines: `findContours` turns each white blob into an
**outline** (a list of points). Use `RETR_EXTERNAL`: you only want the outside of
each blob. Draw the outlines on the camera window so you can **see** them.

Then decide what each outline is. There's **no single right answer**. Here are
some measurements you can compute from an outline. Look them up, print them for a
cube and for a sphere, and compare:

| Measurement | How | Sphere | Cube |
|---|---|---|---|
| **Corners** | `cv2.approxPolyDP` on the outline, count the points | many (8+) | 4 face-on, **6** at an angle |
| **Circularity** | `4π × area / perimeter²` | about 0.9 (1.0 in theory, but pixel outlines are jagged) | about 0.785 for a square |
| **Fill of enclosing circle** | area / area of `cv2.minEnclosingCircle` | close to 1.0 | lower |

Careful: a cube seen **at an angle** shows its front face *and* a strip of its top,
so its outline is a **hexagon**, and a hexagon is fairly round. `--check` tests
that case. Does one measurement on its own cope, or do you need two?

💡 **Print your measurements on the screen** (`cv2.putText`) next to each object.
You'll tune much faster when you can see the numbers change as you move an
object around.

> **Checkpoint:** `--check` says `Step 4 ... ok`. It tests circles, squares,
> tilted squares and angled cubes at three sizes.

---

### Step 5: every colour, every object, labelled

**Goal:** the finished behaviour: every object of every colour, outlined and
labelled `"<colour> <shape>"`, all at once.

1. Write **`detect(frame)`**: for each colour in `COLOURS`, build the mask, find
   the outlines, throw away tiny ones (they're noise, not objects), classify the
   rest. Return a **list of dictionaries**, one per object, each with at least
   `"colour"` (the name), `"shape"` and `"centre"` (`(x, y)` in pixels;
   look up `cv2.moments`). Add any other keys you need for drawing.
2. Write **`draw_detections(frame, detections)`**: draw each outline and its
   label on the frame. Make the label readable on any background.
3. In `main()`: grab → `detect` → `draw_detections` → show. Add a summary line at
   the top of the window, for example `red cube, blue sphere`, or `nothing found`.

Keep **finding** separate from **drawing**: a robot that drives toward the blue
sphere needs the list from `detect()`, not a picture.

> **Checkpoint:** every line of `--check` says `ok`:
>
> ```
> All checks pass. Now make it work on the robot: README, Step 6.
> ```

---

### Step 6: run it on the robot

`--check` uses perfect, flat colours. The robot's camera doesn't: colours shift
with the lighting, shiny objects have bright spots, and the table reflects.

1. `python run_robot.py`, then click **Open Camera**.
2. Hold up or place each of the 8 objects (4 colours × cube/sphere) in front of
   the camera. Aim the camera with the camera pad in the main window.
3. If a colour isn't found, or is found where it shouldn't be, **re-tune its
   range with your trackbars** on the real camera, and update `COLOURS`. Run
   `--check` again afterwards: it should still pass.
4. Use `p` to save pictures of anything that goes wrong, and debug that exact
   frame with `python vision.py pictures/<file>.jpg`.

It doesn't have to be perfect: it has to **work**.

> **Checkpoint:** the 8 objects are labelled correctly in front of the robot,
> several at once.

---

## 4. Troubleshooting

Try an AI tool first (see the top of this README). These are the usual ones:

| Problem | Likely cause |
|---|---|
| `ModuleNotFoundError: No module named 'cv2'` | `pip install -r requirements.txt`, using the **same** Python you run the program with |
| `--check` Setup: "not done yet" or "requirements.txt is missing ..." | You still have the Lab 2 `requirements.txt`. Copy the Lab 3 one over it (Setup, 1.2) |
| `--check`: "could not import your Lab 2 code" | `vision.py` and `lab3_check.py` aren't in your `Lab_2` folder, or you aren't running from it |
| `--check`: "skipped - no display available" | Stage 1 needs a screen. Run the check on the lab computer, not over SSH |
| Window is grey or frozen | No `cv2.waitKey(...)` in your loop |
| `.read()` gives `None` / `error: (-215)` | The source didn't open. Robot: are you on its Wi-Fi? Does the URL work in a browser? |
| Webcam won't open on Windows | Try another index (`1`), or `cv2.VideoCapture(0, cv2.CAP_DSHOW)` |
| Mask is all black | HSV range wrong: hue 0 to 179, not 0 to 360? Red needs two ranges |
| Mask is all white | S min / V min too low: you're matching grey and white too |
| Clicking **Open Camera** freezes the main window | Your button waits for `vision.py` to finish. Re-read Stage 1 |
| The robot camera view lags behind | Frames queue up while your code is busy. Ask an AI tool how to always read the *newest* frame from a stream |
| Pictures are saved in an unexpected folder | Relative paths are relative to where you **ran** the program from |

---

## 5. Demo checklist

Show your TA:

1. `python vision.py --check`: **every line `ok`**.
2. **Stage 1:** your Lab 2 window, **Open Camera** opens `vision.py`, and you can
   still drive and aim the camera while it's open.
3. **Stage 2:** the live robot camera with the 8 objects (red, green, blue and
   yellow; cube and sphere) labelled correctly, several at once.
4. The mask window, and how you tuned the colour ranges.
5. Your `classify_shape()`: what it measures, and why that separates cubes from
   spheres.
6. **How you got unstuck:** the AI chats or documentation you used. Be ready to
   explain any line of `vision.py` the TA points at.
