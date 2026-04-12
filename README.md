# 8-Ball Pool

A browser-based 8-ball pool game with a custom physics engine written in C, exposed to Python via SWIG bindings, and served through a Python HTTP backend.

**[Play it live](https://eight-ball-3cq4.onrender.com)**

> Note: hosted on Render's free tier so the page might take ~ 60 seconds to wake up and load. Refresh once and it will be up.

---

## How It Works

### Physics Engine (C)

The core simulation is written in C (`phylib.c` / `phylib.h`). It models the full physics of a pool table:

- **Ball types**: still balls and rolling balls, each with position, velocity, and acceleration vectors
- **Object types**: balls, holes, horizontal cushions, and vertical cushions — all stored in a tagged union (`phylib_object`) for uniform handling
- **Simulation**: `phylib_roll` advances a ball's position and velocity over a time step using kinematic equations with drag deceleration (`150 mm/s²`)
- **Collision detection**: `phylib_distance` computes geometry-aware distances between any two object types (ball-ball, ball-hole, ball-cushion), and `phylib_bounce` resolves elastic collisions
- **Segmented simulation**: `phylib_segment` advances the table until the next collision event, enabling frame-by-frame animation without simulating the entire shot at once

### Python Bindings (SWIG)

`phylib.i` defines a SWIG interface that wraps the C structs and functions into a Python module. This lets `Physics.py` work with C-level objects directly — no data marshalling overhead.

The `makefile` handles the full build chain:

1. Compile `phylib.c` → `phylib.o`
2. Link into a shared library → `libphylib.so`
3. Run SWIG on `phylib.i` → `phylib_wrap.c` + `phylib.py`
4. Compile the wrapper → `_phylib.so`

### Python Layer (`Physics.py`)

Wraps the SWIG-generated bindings into clean Python classes:

| Class                          | Description                                                          |
| ------------------------------ | -------------------------------------------------------------------- |
| `StillBall` / `RollingBall`    | Ball objects with SVG rendering methods                              |
| `Hole`, `HCushion`, `VCushion` | Table boundary objects                                               |
| `Table`                        | Iterable container of all objects; renders full SVG frames           |
| `Database`                     | SQLite interface for persisting game and shot state                  |
| `Game`                         | Orchestrates a full game session; runs the physics loop on each shot |

The `Game.shoot()` method runs the segmented simulation loop, collecting every intermediate table state as an SVG frame. These frames are sent back to the browser as a single response and animated client-side.

### Backend (`Server.py`)

A lightweight HTTP server built on Python's standard `http.server` module — no frameworks.

| Route                | Method | Description                                                                      |
| -------------------- | ------ | -------------------------------------------------------------------------------- |
| `/` or `/shoot.html` | GET    | Game setup page (player names, game ID)                                          |
| `/display.html`      | POST   | Creates or loads a game, returns the initial table                               |
| `/shot`              | POST   | Accepts cue ball velocity, runs physics simulation, returns all animation frames |
| `/display.css`       | GET    | Stylesheet                                                                       |

### Frontend (`game.js` + `shoot.html`)

The frontend is plain HTML, CSS, and jQuery — no framework.

- Players aim by clicking and dragging from the cue ball; a directional line is drawn in real time using SVG
- On mouse release, the drag vector is converted to a velocity and POSTed to `/shot`
- The server returns all animation frames joined by a delimiter (`:,:`)
- The client splits and renders them sequentially using `setTimeout`, producing smooth animation
- Ball assignment (solids/stripes) is determined automatically after the break by counting which ball type was pocketed first
- Win condition is detected client-side by checking for the absence of the 8-ball in the SVG

### Data Persistence (SQLite)

Game state is stored in `phylib.db` with a normalized schema:

```
Ball → BallTable ← TTable ← Game → Player
                               ↑
                             Shot → TableShot
```

Each shot saves only the final table state, keeping the database small while preserving enough history to resume a game by ID.

---

## Tech Stack

| Layer              | Technology                        |
| ------------------ | --------------------------------- |
| Physics simulation | C (clang, -std=c99)               |
| Python bindings    | SWIG                              |
| Backend            | Python 3.12, stdlib `http.server` |
| Database           | SQLite3                           |
| Frontend           | HTML, CSS, jQuery                 |
| Deployment         | Docker on Render                  |

---

## Running Locally

**Requirements:** `clang`, `swig`, `python3.12`, `make`

```bash
make
python Server.py 8080
```

Then open [http://localhost:8080](http://localhost:8080).
