# PROJECT_BIBLE — SimArcade family (SimArcade, arcade-hangout-hub, Driftcade)

- **Generated:** 2026-10-17
- **Owner:** Red (GitHub user `sredman42`)
- **Scope:** the older SimArcade / arcade-hangout-hub / Driftcade repositories, a sim-racing kiosk launcher for a drift shop sim rig. The project uses Assetto Corsa, Content Manager, MOZA Pit House, and Meta/Oculus VR.
- **Method:** every repository was read from a full clone under `/home/claude/<repo>`. The review covered all remote branches (`git branch -a`), every commit (`git log --all --stat`) and the source files. Vendored or generated content was skipped: `node_modules`, the PyInstaller `build/` folders, Edge browser profile caches and `.exe` binaries. Claims cite file paths. Anything marked **(inference)** is the author's reading of the code, not something a file says outright.
- **Secrets policy:** no passwords, tokens or keys are copied into this document. Where one exists, this document says "a credential is stored in <path>", and every such case is listed under Known Issues (section 7).

## Repositories covered and their HEAD commits

| Repo (GitHub `sredman42/...`) | Local clone path | Branches | HEAD of default branch (`main`) | Other branch heads |
|---|---|---|---|---|
| `simarcade_app` | `/home/claude/simarcade_app` | main | `54ae8b0` 2025-12-07 "Initial commit" | — |
| `simarcade_appv1` | `/home/claude/simarcade_appv1` | main, **optimization-v2** | `9ae77dd` 2025-12-09 "pre-claude save" | `optimization-v2` = `b5c892c` 2025-12-10 "v2 pre" (one commit ahead of main) |
| `arcade-hangout-hub` | `/home/claude/arcade-hangout-hub` | main | `e510c8a` 2025-12-07 "Implement 350Z inspired UI" | — |
| `arcade-hangout-hub-5b3f79ce` | `/home/claude/arcade-hangout-hub-5b3f79ce` | main | `e510c8a` (identical to arcade-hangout-hub) | — |
| `arcade-hangout-hub-9bce0a60` | `/home/claude/arcade-hangout-hub-9bce0a60` | main | `e510c8a` (identical) | — |
| `arcade-hangout-hub-b0453b6e` | `/home/claude/arcade-hangout-hub-b0453b6e` | main | `e510c8a` (identical) | — |
| `arcade-hangout-hub-54a7b831` | `/home/claude/arcade-hangout-hub-54a7b831` | main | `40fae53` 2025-12-09 "Integrate backend API and status" | — |
| `arcade-hangout-hub-a419e26a` | `/home/claude/arcade-hangout-hub-a419e26a` | main | `40fae53` (identical to -54a7b831) | — |
| `arcade-hangout-hub-72afe629` | `/home/claude/arcade-hangout-hub-72afe629` | main | `ae31a4f` 2025-12-11 "Refine AttractMode visuals" | — |
| `simarcade-updates` | `/home/claude/simarcade-updates` | main | `dcb2798` 2025-12-10 "Create index.html" | — |
| `simarcade_v3.0` | `/home/claude/simarcade_v3.0` | main | `3f095de` 2025-12-11 "Initial commit" | — |
| `driftcade` | `/home/claude/driftcade` | main | `b54232a` 2025-12-14 "Add run_updater controller with GitHub primary and email fallback" | — |
| `drift-car-downloads` | `/home/claude/drift-car-downloads` | main | `acdb341` 2026-01-26 "Create infiniti_g35_coupe_2006.zip" | — |

Other clones in `/home/claude` are outside this bible's scope and were not analysed here: `assettoserver-ghostdrift`, `claude-mods`, `redline-damage` and `track-builder`.

---

## Repo lineage & which repo is canonical

### Lineage summary (chronological)

1. **`simarcade_app`** (2025-12-07 12:44 CST). The first attempt, holding only `.gitattributes`. It is an empty placeholder that was abandoned about 20 minutes later in favour of `simarcade_appv1`.
2. **`arcade-hangout-hub`** (Lovable / gpt-engineer project). On 2025-12-07 04:44 UTC (2025-12-06 22:44 CST) Lovable generated the "350Z inspired" React UI in commit `e510c8a`. This is the **UI design source** for SimArcade.
3. **`simarcade_appv1`** (2025-12-07 → 2025-12-10). This is the **actual working SimArcade v1 app**: a Python backend, an Edge kiosk launcher, a React UI, PyInstaller builds and an email over-the-air updater.
   - Commit `fadb9f9` (".16 tested") imported the Lovable UI twice: as the folder `arcade-hangout-hub-main/` and as the root `src/` + `package.json` app.
   - Branch `optimization-v2` (commit `b5c892c`) adds a fully restructured **SimArcade v2.0** in `SimArcade_v2.0/` (Flask, modular backend, `.env` credentials) together with a code generator script.
4. **Lovable remix variants of arcade-hangout-hub** (the 8-hex suffix repos). These are remixes and forks of the same Lovable project, and every one shares the root commit `534a5a9`.
   - `-5b3f79ce`, `-9bce0a60` and `-b0453b6e` have the same commit (`e510c8a`) and the same tree hash (`5f1fb8e…`) as `arcade-hangout-hub`. They are **exact duplicates with no unique content**.
   - `-54a7b831` and `-a419e26a` are at `40fae53` with identical trees (`3a08cbf…`). They add the **backend API integration**: `src/lib/api.ts`, `src/components/ConnectionStatus.tsx` and a health-polling launcher. They are **duplicates of each other**.
   - `-72afe629` is at `ae31a4f` and is a strict superset of all the others. It adds the **Attract Mode UI scaffold** in `src/components/attract/*`. It is the **newest and most complete UI repo**.
5. **`simarcade-updates`** (2025-12-10). A static "mobile-friendly update portal" (`index.html`) meant to let Red download update files from a phone. It belongs to the email update workflow.
6. **`simarcade_v3.0`** (2025-12-11). Holds only a README. It is a **plan** for v3: "Arcade-style sim racing launcher with state machine, diagnostics, and experience system. Production kiosk software for shop sim rig."
7. **`driftcade`** (2025-12-12 → 2025-12-14). The **rebrand and successor** of SimArcade: "Driftcade — Arcade-style sim racing launcher" (`/home/claude/driftcade/README.md`). So far it contains only a folder skeleton and a robust **auto-update subsystem** (GitHub primary with email fallback, backups and rollback) in `tools/`.
8. **`drift-car-downloads`** (2026-01-26). A content repo holding one Assetto Corsa car mod zip, `infiniti_g35_coupe_2006.zip` (about 94.6 MB).

### Lineage table

| Repo | Purpose | First → last commit date | Commits (all branches) | Branches | Status / verdict |
|---|---|---|---|---|---|
| `simarcade_app` | Empty first repo | 2025-12-07 → 2025-12-07 | 1 | main | **Abandoned** (empty) |
| `simarcade_appv1` | SimArcade v1 working app: Python backend, Edge kiosk, React UI, email OTA updater, PyInstaller release; branch `optimization-v2` holds the v2.0 restructure | 2025-12-07 → 2025-12-10 | 12 (11 on main + 1 on optimization-v2) | main, optimization-v2 | **Canonical for SimArcade runtime code.** Use `optimization-v2` for the cleanest backend design and `main` for the version that was actually tested on the rig |
| `arcade-hangout-hub` | Lovable-generated 350Z-styled launcher UI (mock handlers only) | 2025-01-01 (template) → 2025-12-07 | 3 | main | Superseded; identical to 3 variants |
| `arcade-hangout-hub-5b3f79ce` | Lovable remix | same as above | 3 | main | **Exact duplicate** of arcade-hangout-hub (same tree hash) |
| `arcade-hangout-hub-9bce0a60` | Lovable remix | same | 3 | main | **Exact duplicate** |
| `arcade-hangout-hub-b0453b6e` | Lovable remix | same | 3 | main | **Exact duplicate** |
| `arcade-hangout-hub-54a7b831` | Lovable remix + backend API wiring | → 2025-12-09 | 5 | main | Superseded by -72afe629 |
| `arcade-hangout-hub-a419e26a` | Lovable remix + backend API wiring | → 2025-12-09 | 5 | main | **Exact duplicate** of -54a7b831 |
| `arcade-hangout-hub-72afe629` | Lovable UI + API wiring + Attract Mode scaffold | → 2025-12-11 | 9 | main | **Canonical UI repo** (superset of all hub variants) |
| `simarcade-updates` | Static phone download portal for update files | 2025-12-10 | 2 | main | Stub; links point to files that are not in the repo |
| `simarcade_v3.0` | v3 vision README only | 2025-12-11 | 1 | main | **Plan only** |
| `driftcade` | Rebranded successor; skeleton + auto-updater (GitHub + email fallback) | 2025-12-12 → 2025-12-14 | 6 | main | **Latest code in the family**; canonical for updater design |
| `drift-car-downloads` | Hosts an Assetto Corsa car mod zip | 2026-01-26 | 1 | main | Content asset only |

### Canonical pointers ("where is the latest X?")

- **Latest backend / process launcher logic:** `simarcade_appv1`, branch `optimization-v2`, at `SimArcade_v2.0/backend/sim_arcade_logic.py` (Flask). The v1 version tested on the rig is `simarcade_appv1` `main:sim_arcade_logic.py` (http.server, "v0.18 Nuclear Shutdown").
- **Latest UI design:** `arcade-hangout-hub-72afe629`, at `src/components/SimArcadeLauncher.tsx` and `src/components/attract/*`.
- **The UI that actually shipped in the v1 release build:** `simarcade_appv1` `main:src/components/SimArcadeLauncher.tsx`, compiled to `SimArcade_Release/web_ui_build/`.
- **Latest updater design:** `driftcade` `main:tools/` (`update_manager.py`, `github_updater.py`, `email_updater.py`, `run_updater.py`).
- **Latest vision statement:** `simarcade_v3.0/README.md` and the `driftcade` folder skeleton (`backend/ config/ core/ experiences/ frontend/ profiles/ services/ tests/ tools/`).
- **Inference:** the owner says the work later moved to newer GitHub repos and was done mostly on the "Sim PC". These repos are a December 2025 snapshot, captured from the laptop / early rig phase. Paths in `simarcade_appv1/config.json` use `C:\Users\sredm\...` while `SimArcade_Release/config.json` uses `C:\Users\Sredm\...`, which may show two machines or two user profile spellings (inference).

---

## 1. Executive Summary

- **What SimArcade is:** a Windows kiosk-style launcher for a shop sim racing rig built around Assetto Corsa drifting. One click on a big fullscreen button ("VR MODE" or "MONITOR MODE") runs the whole startup sequence:
  - starts MOZA Pit House (wheel and pedal software) minimized and waits for it,
  - in VR mode, also starts the Meta/Oculus client and waits for it,
  - edits Assetto Corsa's `video.ini` `[CAMERA] MODE=` to `OCULUS` (VR) or `DEFAULT` (monitor),
  - launches Content Manager.

  Power, exit and shutdown buttons kill all of these processes again. Source: `simarcade_appv1/sim_arcade_logic.py`, functions `start_session`, `exit_session` and `shutdown_app`.
- **How it is delivered:**
  - A Python backend runs an HTTP server on `127.0.0.1:51234`. It serves the built React UI (`web_ui_build/`) and the JSON command endpoints.
  - `launcher.py` opens Microsoft Edge in `--app` / `--start-fullscreen` mode with a dedicated `--user-data-dir=edge_profile`, which makes it a kiosk.
  - PyInstaller packages `SimArcade.exe` (the launcher) and `Setup.exe` (an auto-detect config wizard) into `SimArcade_Release/`.
- **Remote updates:** Red built an "over-the-air" pipeline that runs phone → Gmail → PC. In `simarcade_appv1/email_monitor.py`, the app reads the newest unread Gmail message over IMAP, saves its attachments and deploys them into the app folder. Zips are expanded, and a smart-path naming rule `src__ui__file.txt` maps to `src/ui/file.txt`. This was proven with joke and test files (`src/ui/simarcade_joke.txt`, `voice_test.txt`, `email_updates/*`).
- **Evolution:**
  - v1 (`simarcade_appv1` main) → v2.0 restructure (`optimization-v2`): Flask, `ProcessManager` with PID tracking, `ConfigManager` validation, rotating logs, `.env` credentials, frontend retry/health API client and a single `build_master.bat`.
  - Then a v3 vision (`simarcade_v3.0`: state machine, diagnostics, experience system).
  - Then the **Driftcade** rebrand (`driftcade`), which so far contains a hardened updater: GitHub polling first, a checksum-verified and sender-whitelisted email fallback, staging, backups (keep 3) and rollback.
- **UI design:** produced in Lovable (`arcade-hangout-hub*`). It is a "350Z inspired" dark theme with hot-pink neon primary (`--primary: 330 90% 55%`), gold secondary (`--secondary: 40 70% 45%`), deep maroon, Orbitron/Rajdhani fonts and a 3-image drift background slideshow. The final Lovable variant (`-72afe629`) adds an "Attract Mode" kiosk screen scaffold: media display (static, carousel or video), a big "Touch to Start" control and scanlines.
- **Keywords:** SimArcade, Sim Arcade, Driftcade, arcade-hangout-hub, Lovable, gpt-engineer, kiosk, attract mode, Assetto Corsa, acs.exe, Content Manager, MOZA Pit House, Oculus, Meta Quest, VR mode, monitor mode, video.ini, Edge app mode, PyInstaller, Setup.exe, email updater, IMAP, Gmail, GitHub updater, rollback, drift shop, sim rig.

---

## 2. Tech Stack & Dependencies

### 2.1 Backend (Python, Windows only)

- **SimArcade v1** (`simarcade_appv1` main):
  - Uses the Python standard library `http.server` (`HTTPServer` and `BaseHTTPRequestHandler`), `subprocess`, `threading` and `json`.
  - The one third-party dependency is **psutil**. `Run_App.bat` auto-installs it with `python -m pip install psutil`.
  - Windows-specific code: `subprocess.STARTUPINFO` with `wShowWindow = 7` (minimized), `winreg` in `setup_wizard.py` (Steam path from `HKCU\Software\Valve\Steam`), and `taskkill`.
  - The Python version is probably **3.14**. Inference from the tracked `__pycache__/sim_arcade_logic.cpython-314.pyc`.
- **SimArcade v2.0** (`simarcade_appv1` branch `optimization-v2`, `SimArcade_v2.0/`):
  - Runs on **Flask** + **flask-cors**, with psutil and `logging.handlers.RotatingFileHandler`.
  - Pinned requirements appear only inside the generator script `SimArcade_v2.0/simarcade_v2_generator.py` (function `generate_tools`, which writes `tools/requirements.txt`): flask 3.0.0, flask-cors 4.0.0, psutil 5.9.6, pyinstaller 6.3.0, Pillow 10.1.0, requests 2.31.0, watchdog 3.0.0 and pywin32 306. The generated `requirements.txt` itself is **not committed** (see Known Issues).
- **Driftcade updater** (`driftcade/tools/*.py`): pure standard library (`urllib.request`, `imaplib`, `email`, `zipfile`, `hashlib`, `shutil`, `logging`, `argparse`). No third-party packages.
- **Packaging:** **PyInstaller** `--onefile`. Specs: `simarcade_appv1/SimArcade.spec`, `Setup.spec` and `sim_arcade_logic.spec`. v2 specs are `SimArcade_v2.0/build_scripts/specs/SimArcade.spec` (hiddenimports flask, flask_cors, psutil) and `Setup.spec`.

### 2.2 Front-end (TypeScript / React)

- **Lovable template** "new_style_vite_react_shadcn_ts" (root commit `534a5a9` in all hub repos). It is built from:
  - Vite 5.4 with `@vitejs/plugin-react-swc` (dev server on port 8080, host `::`), React 18.3 and TypeScript 5.8,
  - Tailwind CSS 3.4 with `tailwindcss-animate`, shadcn-ui (Radix UI primitives under `src/components/ui/*`) and `lucide-react` icons,
  - `sonner` toasts, `@tanstack/react-query`, `react-router-dom` 6, and `lovable-tagger` (dev-mode component tagger in `vite.config.ts`).
  - Source: `simarcade_appv1/package.json` and `arcade-hangout-hub*/package.json`.
- **v2.0 frontend** (`SimArcade_v2.0/frontend/package.json`, name `simarcade-v2-ui` 2.0.0) is slimmed down to react, react-dom, react-router-dom, react-query, sonner, lucide-react, clsx, tailwind-merge, cva, `@radix-ui/react-slot` and tailwindcss-animate. It drops the full shadcn set and lovable-tagger.
- **Fonts:** Orbitron and Rajdhani from Google Fonts (`arcade-hangout-hub-72afe629/index.html`, `tailwind.config.ts` `fontFamily.display` / `fontFamily.body`).

### 2.3 External applications controlled (from `config.json` keys)

| Config key (`paths.*`) | Application | Process name watched | Source |
|---|---|---|---|
| `content_manager` | Assetto Corsa **Content Manager** (`Content Manager.exe`) | `Content Manager.exe` | `simarcade_appv1/sim_arcade_logic.py` `PROC_CM` |
| `video_ini` | Assetto Corsa `Documents\Assetto Corsa\cfg\video.ini` | — | `set_video_mode()` |
| `meta_client` | Meta/Oculus PC app (`oculus-client\Client.exe`) | `OculusClient.exe` | `PROC_META` |
| `moza_pithouse` | **MOZA Pit House** (wheelbase software) | `MOZA Pit House.exe` | `PROC_MOZA` |
| — | Assetto Corsa game | `acs.exe` | `PROC_AC` |
| — | Microsoft Edge (kiosk window) | `msedge.exe` | `launcher.py` |

- **Timeouts:** `timeouts.meta_launch` = 20.0 s and `timeouts.moza_launch` = 10.0 s. **Server:** `server.host` = 127.0.0.1 and `server.port` = 51234. Source: `simarcade_appv1/config.json`.

### 2.4 Services

- **Gmail IMAP** (`imap.gmail.com:993`) carries email updates in `simarcade_appv1/email_monitor.py`, `SimArcade_v2.0/tools/email_monitor.py` and `driftcade/tools/email_updater.py`.
- **GitHub REST API** (`api.github.com`) and `raw.githubusercontent.com` carry Driftcade's primary updates (`driftcade/tools/github_updater.py`). The repo watched is `sredman42/Driftcade` on branch `main`.
- **Lovable** (lovable.dev) generated the UI. The commits are authored by `gpt-engineer-app[bot]`.

---

## 3. Architectural Overview

### 3.1 Runtime topology (SimArcade v1, `simarcade_appv1` main)

```
SimArcade.exe (PyInstaller of launcher.py)
 ├─ thread: sim_arcade_logic.run_server()  -> HTTPServer 127.0.0.1:51234
 │     GET  /            -> web_ui_build/index.html (static file server)
 │     GET  /<asset>     -> web_ui_build/<asset> (html/js/css/png content types)
 │     GET  /health      -> {"status":"ok","mode":"monitor_active"|"idle"}
 │     POST /start/vr    -> start_session(vr=True)
 │     POST /start/monitor -> start_session(vr=False)
 │     POST /exit        -> shutdown_app()   (v0.18: same as /app/shutdown)
 │     POST /app/shutdown-> shutdown_app()
 └─ main thread: launch_edge_app() -> msedge.exe --app=http://127.0.0.1:51234/ --start-fullscreen
                                       --user-data-dir=<BASE_DIR>/edge_profile --no-first-run
       loop: if backend.SHUTDOWN_REQUESTED -> terminate Edge, exit
             if Edge process exited -> set SHUTDOWN_REQUESTED, exit
```

- Sources: `simarcade_appv1/launcher.py` and `simarcade_appv1/sim_arcade_logic.py`.
- **BASE_DIR resolution:** `get_base_path()` returns `Path(sys.executable).parent` when the app is frozen (PyInstaller) and the script folder otherwise. `config.json`, `web_ui_build/`, `edge_profile/` and `SimArcade_backend_log.txt` all live next to the exe. Source: `sim_arcade_logic.py`.
- **Logging:** `log()` prefixes lines with `[BACKEND] <timestamp> |` and appends them to `SimArcade_backend_log.txt`. The startup banner identifies the version:
  - v0.15 "Config-Based" in `637fa5b`,
  - v0.16 "EXE-Ready" in `fadb9f9`,
  - v0.18 "Nuclear Shutdown" from `a093789` onward.

### 3.2 Session start data flow (VR / Monitor)

1. The UI button calls `fetch("http://127.0.0.1:51234/start/vr", {method:"POST"})` (`simarcade_appv1/src/components/SimArcadeLauncher.tsx`, `sendCommand`).
2. `start_session(vr)` refuses with `"Sim is running. Exit first."` if `Content Manager.exe` or `acs.exe` is already running.
3. Cleanup kills any leftover `acs.exe`, `Content Manager.exe` and `OculusClient.exe`.
4. MOZA Pit House is launched minimized, with a wait of up to `moza_launch` seconds for its process.
5. In VR mode, the Meta client is launched minimized with a wait of `meta_launch` seconds, then `set_video_mode("OCULUS")`. Otherwise `set_video_mode("DEFAULT")` runs. There is a 1 s sleep either way.
6. Content Manager is launched in the normal window state.
7. `monitor_active = True` (protected by `monitor_lock`). The response is `{"status":"ok","message":"Session Started"}`.

- **video.ini edit:** the file is rewritten line by line. Any `MODE=` line inside the `[CAMERA]` section is replaced. Source: `set_video_mode()`.

### 3.3 Shutdown flow ("Nuclear Shutdown", v0.18)

- `shutdown_app()` sets `SHUTDOWN_REQUESTED = True`, calls `exit_session()` (which kills AC, CM, Meta and MOZA) and returns success right away.
- A daemon thread waits 2 s, then runs `os.system("taskkill /F /IM msedge.exe /T")` and `os._exit(0)`. The code comments read "Executing Order 66" and "The Nuclear Option".
- `run_server()` loops `handle_request()` with a 1 s timeout until `SHUTDOWN_REQUESTED`.
- Commit `a093789` "v1.0 Stable - Fullscreen & Shutdown Fixed" introduced the dedicated Edge profile, which makes `edge_process.poll()` reliable ("prevent process hand-off"), and this shutdown logic.

### 3.4 State management

- **Backend:**
  - v1 holds module globals `monitor_active`, `monitor_lock` and `SHUTDOWN_REQUESTED`.
  - v2 replaces `SHUTDOWN_REQUESTED` with `threading.Event` `shutdown_event`, and adds a `ProcessManager.tracked_processes` dict of `psutil.Popen` handles keyed by "moza", "meta" and "cm".
  - **(inference)** In v2, `start_session` launches processes under keys like `"moza"` but kills by process names like `"MOZA Pit House.exe"`. Kills therefore fall back to name-substring matching and the PID tracking is never used for kills.
- **Frontend:**
  - Local React state only. `isLoading` and `mounted` drive the entrance animations in v1.
  - The hub variants -54a7b831, -a419e26a and -72afe629 add `isConnected` and `isCheckingConnection`, polling `/health` every 5 s.
  - v2.0 adds `isHealthy`, polling every 10 s and disabling the mode buttons while the backend is unhealthy.
  - No global store. React Query is installed and its provider is mounted, but it is not used for these calls.

### 3.5 Front-end ↔ back-end communication

- Transport: plain `fetch` over HTTP to the hard-coded `http://127.0.0.1:51234`. The backend sends `Access-Control-Allow-Origin: *` (v1) or uses `CORS(app)` (v2), so the Vite dev server on :8080 can call it.
- The response contract is `{"status": "ok"|"error", "message": str}`, and the HTTP status is always 200 for known routes. The frontends read it differently:
  - `simarcade_appv1/src/components/SimArcadeLauncher.tsx` checks `response.ok` and shows `data.message`.
  - `arcade-hangout-hub-72afe629/src/lib/api.ts` declares `ApiResponse {success, message?, error?}`, throws only on a non-OK HTTP status, and treats anything else as success.
  - `SimArcade_v2.0` `frontend/src/lib/api.ts` (it exists only inside the generator) does 3 retries with linear backoff (1 s × attempt), a 5 s `AbortSignal.timeout` and a 2 s health check timeout.

### 3.6 Updater flows

**A. SimArcade v1 email pipeline** (`simarcade_appv1/email_monitor.py`, plus the reverted `email_update_daemon.py`)

1. The phone sends an email with attachments to the shop Gmail inbox. Credentials are hard-coded in the file (see Known Issues).
2. `connect_imap()` logs in. `fetch_latest_unseen()` searches `UNSEEN` and fetches only the **last** unseen message.
3. `process_attachments()` saves each attachment to `<DEPLOY_ROOT>/email_updates/`. A `.zip` is extracted by basename into `email_updates/` and each inner file is deployed. Any other file is deployed directly.
4. `smart_deploy_path()` maps `src__a__b__name.ext` to `<DEPLOY_ROOT>/src/a/b/name.ext`. Any other name goes to `<DEPLOY_ROOT>/<name>`.
5. `DEPLOY_ROOT` is hard-coded to `c:\Users\Sredm\Documents\GitHub\SimArcade_AppV1`.
6. The daemon wrapper `email_update_daemon.py` polls every 60 s and logs to `SimArcade_email_daemon_log.txt`. It was added in `563ef23` "fully working email pipe" and **reverted** in `8a076d2`. It survives only in history (`git show 563ef23:email_update_daemon.py`).
7. Proof-of-pipeline artifacts:
   - `email_updates/simarcade_joke_ui_update.zip` contains `src__pages__Index.tsx`, a "Garage Wisdom" joke banner page,
   - `email_updates/simarcade_multi_test_files.zip` contains `multi_test_1..3.txt`,
   - also `src/ui/deep_test.txt`, `src/ui/simarcade_joke.txt` ("DevOps: Dad Edition"), `voice_test.txt`, `ui_test_update.py` and `ui_test_update_v3.py`.

**B. SimArcade v2.0 email monitor** (`SimArcade_v2.0/tools/email_monitor.py`, branch optimization-v2)

- The same logic, but credentials come from environment variables `SIMARCADE_EMAIL` and `SIMARCADE_EMAIL_PASSWORD` (template at `SimArcade_v2.0/.env.template`, placeholders only). `DEPLOY_ROOT` is `Path(__file__).parent.parent`.

**C. Phone download portal** (`simarcade-updates/index.html`)

- A static page listing `config.json` ("Oculus path fixed"), `setup_wizard.py` ("Oculus detection fixed"), `requirements.txt` and `backend/sim_arcade_logic.py`, each with a Download button.
- The instructions say: "Upload to Google Drive or email to your update system → Deploy to your SIM rig", and "For Other AIs: Share this repo github.com/sredman42/SimArcade-Updates".

**D. Driftcade updater** (`driftcade/tools/`), the most mature design

- `run_updater.py` `UpdateRunner`:
  - polls every 60 s (`POLL_INTERVAL`),
  - tries `GitHubUpdater.check_for_updates()`, then `deploy_updates()`,
  - after 3 consecutive GitHub failures (`GITHUB_FAIL_THRESHOLD`), tries `EmailUpdater.run_once()` at most every 300 s (`EMAIL_CHECK_INTERVAL`),
  - logs to `<root>/logs/updater.log`,
  - takes CLI flags `--once` and `--root <path>`.
- `github_updater.py` `GitHubUpdater`:
  1. Reads `GITHUB_TOKEN` from `<root>/.env`.
  2. Gets the latest commit with `GET /repos/sredman42/Driftcade/commits/main`.
  3. Diffs with `/compare/<last_sha>...main`. The first run instead lists everything with `/git/trees/main?recursive=1`.
  4. Filters to allowed paths, takes a backup, downloads each file from `raw.githubusercontent.com`, stages and deploys.
  5. On deploy failure it calls `rollback()`.
  6. State is kept in `_update_staging/github_state.json` (`last_commit_sha`).
- `email_updater.py` `EmailUpdater`:
  - Only processes UNSEEN mail whose subject **starts with** `[DRIFTCADE-UPDATE]` and whose sender is in `EMAIL_ALLOWED_SENDERS` (comma list in `.env`). Credentials come from `.env` keys `EMAIL_ADDRESS` and `EMAIL_PASSWORD`.
  - Requires one `.zip` plus one `.sha256` or `.checksum` attachment, and verifies SHA-256.
  - Processes only the first valid email per cycle, marks it `\Seen` and records the ID in `_update_staging/email_state.json` (last 100 IDs).
- `update_manager.py` `UpdateManager` (shared by both updaters):
  - `ALLOWED_FOLDERS = ["backend","tools","config","experiences"]`,
  - `PROTECTED_ITEMS = [".env","logs","_backups","_update_staging","frontend"]`, deny by default,
  - `MAX_BACKUPS = 3`, with backups in `_backups/backup_<YYYYmmdd_HHMMSS>_<desc>/` plus `backup_info.json`,
  - staging in `_update_staging/`, `validate_staging()`, `deploy_staged_files()` (copy2), `rollback(backup_name=None)` and `get_file_hash()` (SHA-256),
  - its docstring gives the example project root `D:\Driftcade_v1`.

### 3.7 Build & release flow

- **v1 UI build:** `simarcade_appv1/Build_UI.bat` checks for Node, runs `npm install` and `npm run build`, then renames `dist` to `web_ui_build`.
- **v1 installer build:** `simarcade_appv1/Build_Installer.bat`:
  1. installs pyinstaller and deletes `build`, `dist`, `SimArcade_Release` and `*.spec`,
  2. runs `pyinstaller --noconsole --onefile --name SimArcade launcher.py` and `pyinstaller --console --onefile --name Setup setup_wizard.py`,
  3. moves both exes into `SimArcade_Release/` and xcopies `web_ui_build`.
  - The documented new-rig steps are "1. Run Setup.exe, 2. Run SimArcade.exe".
- **v1 dev run:** `Run_App.bat` runs `python launcher.py`.
- **v2 build:** `SimArcade_v2.0/build_scripts/build_master.bat` (VERSION=2.0.0) runs 7 steps:
  1. checks prerequisites,
  2. installs the pip requirements,
  3. runs npm install in `frontend`,
  4. builds the UI,
  5. moves `frontend\dist` to `web_ui_build` and cleans old builds,
  6. runs pyinstaller with both specs,
  7. assembles `SimArcade_Release` and copies `config.json`.
- **v2 dev run:** `SimArcade_v2.0/Run_App_Dev.bat` runs `python backend\launcher.py`. `README_DEVELOPER.md` describes running the backend and `npm run dev` (http://localhost:8080) in parallel.
- **Setup wizard** (`setup_wizard.py`; v2 copy at `tools/setup_wizard.py`):
  - finds Steam through the registry, finds the Assetto Corsa folder containing `acs.exe` (the Steam library and `C:`, `D:`, `E:` SteamLibrary paths) and finds `Documents\Assetto Corsa\cfg\video.ini`,
  - looks for Content Manager on the Desktop, in `Desktop\CM`, and in the AC folder, and checks fixed paths for Oculus and MOZA,
  - writes `config.json` to the **current working directory**.

---

## 4. Directory Structure & Code Map

### 4.1 `simarcade_appv1` — branch `main` (HEAD `9ae77dd`)

Repo path: `/home/claude/simarcade_appv1`. About 1150 tracked files, of which about 880 are Edge browser profile files and about 30 are PyInstaller build intermediates.

| Where X lives | Path |
|---|---|
| Backend HTTP server + process orchestration | `sim_arcade_logic.py` (243 lines) |
| Kiosk launcher (starts server thread + Edge app window) | `launcher.py` (70 lines) |
| Auto-configuration wizard (Setup.exe source) | `setup_wizard.py` (103 lines) |
| Email OTA updater (current) | `email_monitor.py` (193 lines; docstring calls it `email_monitor_zip.py`) |
| Email OTA updater (previous version, kept) | `email_monitor old.py` (148 lines) |
| Runtime config (dev) | `config.json` |
| Runtime config (release) | `SimArcade_Release/config.json` |
| Release executables | `SimArcade_Release/SimArcade.exe`, `SimArcade_Release/Setup.exe`, `SimArcade_Release/sim_arcade_logic.exe` (added in `9ae77dd`) |
| Built UI served by backend | `web_ui_build/` (dev) and `SimArcade_Release/web_ui_build/` (release) |
| React UI source (root Vite app) | `src/` — `src/main.tsx`, `src/App.tsx`, `src/pages/Index.tsx`, `src/components/SimArcadeLauncher.tsx`, `BackgroundSlideshow.tsx`, `ArcadeButton.tsx`, `SecondaryControls.tsx`, `NavLink.tsx`, `src/components/ui/*` (shadcn), `src/index.css`, `tailwind.config.ts`, `vite.config.ts`, `package.json` |
| Drift background images | `src/assets/drift-bg-1.png`, `drift-bg-2.png`, `drift-bg-3.png` |
| Imported copy of Lovable project | `arcade-hangout-hub-main/` (a full copy of the arcade-hangout-hub repo, with a wired `SimArcadeLauncher.tsx`) |
| Email update landing folder + test payloads | `email_updates/` (`simarcade_joke_ui_update.zip`, `simarcade_multi_test_files.zip`, `src__pages__Index.tsx`, `src__ui__deep_test.txt`, `src__ui__simarcade_joke.txt`, `voice_test.txt`, `ui_test_update*.py`, `multi_test_*.txt`, `Does this work.txt`) |
| Smart-path deploy test outputs | `src/ui/deep_test.txt`, `src/ui/simarcade_joke.txt`, root `multi_test_*.txt`, `voice_test.txt`, `ui_test_update*.py` |
| Build scripts | `Build_UI.bat`, `Build_Installer.bat`, `Run_App.bat` |
| PyInstaller specs | `SimArcade.spec`, `Setup.spec`, `sim_arcade_logic.spec` |
| PyInstaller intermediates (should not be tracked) | `build/Setup/`, `build/SimArcade/`, `build/sim_arcade_logic/` |
| Edge kiosk browser profile (should not be tracked) | `edge_profile/`, `SimArcade_Release/edge_profile/` |
| Backend logs (tracked) | `SimArcade_backend_log.txt`, `SimArcade_Release/SimArcade_backend_log.txt`, `__pycache__/SimArcade_backend_log.txt` |
| README | `README.md` (unmodified Lovable boilerplate, "REPLACE_WITH_PROJECT_ID") |

### 4.2 `simarcade_appv1` — branch `optimization-v2` (HEAD `b5c892c`), folder `SimArcade_v2.0/`

This commit adds `SimArcade_v2.0/` alongside everything from main.

| Where X lives | Path |
|---|---|
| Entry point (server thread + Edge app) | `SimArcade_v2.0/backend/launcher.py` |
| Flask server, routes, session logic | `SimArcade_v2.0/backend/sim_arcade_logic.py` (227 lines) |
| Process launch/kill with PID tracking | `SimArcade_v2.0/backend/process_manager.py` (`ProcessManager`) |
| Config load + validation | `SimArcade_v2.0/backend/config_manager.py` (`ConfigManager`) |
| Rotating log setup (5 MB × 3) | `SimArcade_v2.0/backend/logger_setup.py` (`setup_logging`) |
| Setup wizard | `SimArcade_v2.0/tools/setup_wizard.py` |
| Env-var based email monitor | `SimArcade_v2.0/tools/email_monitor.py` |
| Master build | `SimArcade_v2.0/build_scripts/build_master.bat` |
| PyInstaller specs | `SimArcade_v2.0/build_scripts/specs/SimArcade.spec`, `Setup.spec` |
| Frontend | `SimArcade_v2.0/frontend/` (`src/App.tsx`, `src/main.tsx`, `src/pages/Index.tsx`, `src/components/SimArcadeLauncher.tsx`, `src/index.css`, `vite.config.ts`, `tailwind.config.ts`, `package.json`) |
| Backend API client (NOT committed; only in generator) | intended `SimArcade_v2.0/frontend/src/lib/api.ts`, whose source is in `simarcade_v2_generator.py` `generate_frontend_code()` |
| Python requirements (NOT committed; only in generator) | intended `SimArcade_v2.0/tools/requirements.txt`, whose source is in `simarcade_v2_generator.py` `generate_tools()` |
| One-shot project generator (writes all of v2) | `SimArcade_v2.0/simarcade_v2_generator.py` (1797 lines; functions `create_directory_structure`, `generate_backend_files`, `generate_tools`, `generate_build_scripts`, `generate_config_files`, `generate_frontend_structure`, `generate_frontend_code`, `generate_documentation`, `generate_run_script`, `print_summary`) |
| Docs | `SimArcade_v2.0/README.md` (user), `SimArcade_v2.0/README_DEVELOPER.md` (dev setup, structure, test environments DEV_LAPTOP / HOME_RIG / SHOP_RIG) |
| Env template | `SimArcade_v2.0/.env.template` (keys `SIMARCADE_EMAIL`, `SIMARCADE_EMAIL_PASSWORD`, placeholder values) |
| Config | `SimArcade_v2.0/config.json` (`meta_client` is empty here) |

### 4.3 `arcade-hangout-hub` family (Lovable UI)

The common files below are the same in every variant (template `534a5a9` plus `e510c8a`).

| Where X lives | Path |
|---|---|
| Page entry / routing | `src/main.tsx`, `src/App.tsx` (routes `/` → `Index`, `*` → `NotFound`), `src/pages/Index.tsx` (renders `<SimArcadeLauncher />`) |
| Launcher screen | `src/components/SimArcadeLauncher.tsx` |
| Neon arcade button | `src/components/ArcadeButton.tsx` (variants primary pink / secondary gold) |
| Top-right controls (Debug, Settings, Exit) | `src/components/SecondaryControls.tsx` |
| 30 s crossfading drift background slideshow | `src/components/BackgroundSlideshow.tsx` (`SLIDE_DURATION = 30000`, 1 s fade) |
| Theme tokens (350Z palette, neon glows) | `src/index.css`, `tailwind.config.ts` |
| Background images | `src/assets/drift-bg-1.png`, `drift-bg-2.png`, `drift-bg-3.png` |
| shadcn UI primitives | `src/components/ui/*` |
| HTML shell (title "SimArcade Launcher", Google Fonts) | `index.html` |

Files unique to the later variants:

| Feature | Path | In which repos |
|---|---|---|
| Backend API client (`startVRMode`, `startMonitorMode`, `shutdownApp`, `checkHealth`) | `src/lib/api.ts` | -54a7b831, -a419e26a, -72afe629 |
| Connected/Disconnected pill | `src/components/ConnectionStatus.tsx` | -54a7b831, -a419e26a, -72afe629 |
| Attract Mode orchestrator | `src/components/attract/AttractMode.tsx` | -72afe629 only |
| Attract media layer (static/carousel/video + 6 overlay layers) | `src/components/attract/AttractMediaDisplay.tsx` | -72afe629 only |
| Attract controls overlay ("Touch to Start", VR/Monitor toggle, Exit, optional Settings) | `src/components/attract/AttractControls.tsx` | -72afe629 only |
| Attract button (primary/secondary/danger; default/large/xl) | `src/components/attract/AttractButton.tsx` | -72afe629 only |
| Barrel export | `src/components/attract/index.ts` | -72afe629 only |
| Attract keyframes (`attract-pulse`, `attract-fade`) | `src/index.css` | -72afe629 only |
| `font-display`/`font-body` + `boxShadow.attract-*` | `tailwind.config.ts` | -72afe629 only |

### 4.4 `driftcade` (HEAD `b54232a`)

| Where X lives | Path |
|---|---|
| Update controller (run at startup) | `driftcade/tools/run_updater.py` (`UpdateRunner`) |
| GitHub primary updater | `driftcade/tools/github_updater.py` (`GitHubUpdater`) |
| Email fallback updater | `driftcade/tools/email_updater.py` (`EmailUpdater`) |
| Shared backup/stage/deploy/rollback | `driftcade/tools/update_manager.py` (`UpdateManager`) |
| Empty planned modules (`.gitkeep` only) | `driftcade/backend/`, `config/`, `core/`, `experiences/`, `frontend/`, `profiles/`, `services/`, `tests/` |
| Ignore rules (local runtime folders) | `driftcade/.gitignore` (tail: `logs/`, `_backups/`, `_update_staging/`; also `.env`, `*.spec`) |
| README | `driftcade/README.md` ("Arcade-style sim racing launcher") |

### 4.5 Small repos

- `simarcade_app`: `.gitattributes` only.
- `simarcade-updates`: `index.html` (phone download portal), `README.md` (title only) and `.gitattributes`.
- `simarcade_v3.0`: `README.md` only (v3 vision sentence).
- `drift-car-downloads`: `infiniti_g35_coupe_2006.zip`, an Assetto Corsa car folder `infiniti_g35_coupe_2006/` with 142 entries:
  - `.kn5` models plus LODs b, c and d, `collider.kn5`, `data.acd`, `animations/*.ksanim`, and `sfx/*.bank` + `GUIDs.txt`,
  - `extension/ext_config.ini` (CSP config), `ui/ui_car.json` ("Infiniti G35 2006", "v1.2 by ACTK"),
  - 8 skins (`00_Brilliant Silver Metallic`, `Black Obsidian`, `Crystal Blue`, `Desert Platinum`, `Diamond Graphite`, `Emerald Mist Metallic`, `Garnet Fire Metallic`, `Ivory Pearl`).
  - This is third-party mod content (author ACTK per `ui_car.json`). It is not Red's code.

---

## 5. Core Modules & Features

### 5.1 One-click VR / Monitor session launcher

- **Primary files:** `simarcade_appv1/sim_arcade_logic.py` (`start_session`, `exit_session`, `set_video_mode`, `launch_minimized`, `wait_for_process`) and `SimArcade_v2.0/backend/sim_arcade_logic.py` (branch `optimization-v2`).
- **Repos and branches:** `simarcade_appv1` main (v0.18) and optimization-v2 (v2.0, Flask).
- **Behaviour:** described in section 3.2. VR mode adds the Meta client and sets `video.ini` MODE to `OCULUS`. Monitor mode sets `DEFAULT`.
- **v2 differences:**
  - `ProcessManager.launch()` uses `psutil.Popen`, refuses a duplicate launch of a tracked name, and `kill()` does terminate → wait(3 s) → kill.
  - `/exit` now calls `exit_session()` only. It no longer shuts down the app.
  - `/app/shutdown` calls `shutdown_app()` and then `os._exit(0)` after 1 s.
  - Missing keys fall back to `TIMEOUTS.get(...)` defaults.

### 5.2 Kiosk window (Edge app mode)

- **Files:** `simarcade_appv1/launcher.py` and `SimArcade_v2.0/backend/launcher.py`.
- **Behaviour:**
  - Looks for `msedge.exe` under Program Files (x86) and then Program Files.
  - Starts it with `--app=<url> --start-fullscreen --user-data-dir=<BASE_DIR>/edge_profile --no-first-run --no-default-browser-check`.
  - Watches for the window being closed and for the backend shutdown flag.
- **History:**
  - Initial commit `637fa5b`: no profile dir and no watch loop.
  - `a093789`: added `--user-data-dir` and the two-way shutdown loop ("Fullscreen & Shutdown Fixed").

### 5.3 Static UI server

- **Files:** `simarcade_appv1/sim_arcade_logic.py` `SimHandler.serve_ui_file` (manual content types for html, js, css and png, otherwise octet-stream) and v2 `serve_ui` (Flask `send_from_directory(WEB_DIR, path)`).
- `WEB_DIR = BASE_DIR / "web_ui_build"`.

### 5.4 Launcher UI ("SIM ARCADE — Ready to Race")

- **Shipped v1 UI:** `simarcade_appv1/src/components/SimArcadeLauncher.tsx`.
  - Fullscreen with the `BackgroundSlideshow`, a top-right "DEBUG OFF" pill, a Settings button (toast "Settings locked in arcade mode.") and a Power button (`POST /app/shutdown`).
  - A big gradient "SIM ARCADE" title and "Ready to Race" subtitle.
  - Two large glass buttons: VR MODE (fuchsia, `Headset` icon) and MONITOR MODE (amber, `Monitor` icon).
  - Entrance animations come from the `mounted` state (slide-down, zoom-in, slide-up), added in commit `68c184a` "fade in save".
- **Lovable original:** `arcade-hangout-hub/src/components/SimArcadeLauncher.tsx` uses `ArcadeButton` and `SecondaryControls` with **mock handlers** (toasts only).
- **Lovable wired version:** `arcade-hangout-hub-72afe629/src/components/SimArcadeLauncher.tsx` calls `@/lib/api`, polls health every 5 s and shows `ConnectionStatus`.
- **v2.0 UI:** `SimArcade_v2.0/frontend/src/components/SimArcadeLauncher.tsx` adds an Online/Offline indicator (green or red dot). Buttons are disabled when the backend is unhealthy, and health is polled every 10 s.

### 5.5 Attract Mode (kiosk idle screen) — design scaffold

- **Files:** `arcade-hangout-hub-72afe629/src/components/attract/*` (only in that repo).
- **Design notes:** these are written in the `AttractMode.tsx` header comment.
  - Palette for a "bright workshop + VR": primary hot pink at 330°, secondary gold at 40°, background at 5% lightness.
  - Typography: Orbitron for display, Rajdhani for body.
  - Touch targets at least 48 px.
  - Screen padding 24–56 px.
- **Status:**
  - Handlers are placeholders (`console.log`) and the state is hard-coded (`currentMode = "static"`, `isVRMode = false`).
  - **It is not routed.** `src/pages/Index.tsx` still renders `SimArcadeLauncher`.
- **Implementation notes left for the logic handoff** (in `AttractMode.tsx`):
  1. image carousel with setInterval (about 10 s),
  2. a video interrupt timer (30–45 s) that fades to video and returns on `onEnded`,
  3. VR toggle through `startVRMode()` / `startMonitorMode()`,
  4. exit through `shutdownApp()`,
  5. testing at 1080p and in the VR desktop view.

### 5.6 Auto-configuration wizard (Setup.exe)

- **Files:** `simarcade_appv1/setup_wizard.py` and `SimArcade_v2.0/tools/setup_wizard.py`.
- **Process:** Steam registry lookup, AC detection by `acs.exe`, `video.ini` lookup, then fixed-list detection for Content Manager, Oculus and MOZA. It writes `config.json` and prints `[FOUND]` or `[MISSING]`.
- `simarcade-updates/index.html` mentions a later "Oculus detection fixed" version of `setup_wizard.py` that is **not present** in any repo (inference: it lived on the rig or in a newer repo).

### 5.7 Email OTA updater (v1 / v2)

- **Files:**
  - `simarcade_appv1/email_monitor.py` (main) and `email_monitor old.py`,
  - `SimArcade_v2.0/tools/email_monitor.py` (optimization-v2),
  - history-only: `email_update_daemon.py` and `email_update_daemon_FIXED.py` (`563ef23`, reverted in `8a076d2`).
- **Flow:** see section 3.6 A/B.
- **Status:** the commit message in `563ef23` claims "fully working email pipe", but the daemon was reverted 42 minutes later. The one-shot `email_monitor.py` remains on main.

### 5.8 Driftcade auto-updater (GitHub primary + email fallback)

- **Files:** `driftcade/tools/run_updater.py`, `github_updater.py`, `email_updater.py` and `update_manager.py`.
- **Security features:**
  - subject prefix `[DRIFTCADE-UPDATE]`,
  - sender whitelist,
  - mandatory SHA-256 checksum attachment,
  - allow-listed folders with `frontend` and `.env` protected,
  - backup before every deploy and rollback on failure.
- **Self-tests:** each module has a `__main__` self-test.
  - `update_manager.py` tests path protection for `backend/app.py`, `tools/updater.py`, `.env`, `frontend/index.html` and `logs/debug.log`.
  - `email_updater.py` tests subject validation.
  - `github_updater.py` tests the API connection.

### 5.9 Build / packaging pipeline

- **Files:** `simarcade_appv1/Build_UI.bat`, `Build_Installer.bat`, `Run_App.bat` and `*.spec`, plus `SimArcade_v2.0/build_scripts/build_master.bat` and `specs/*`. See section 3.7.

### 5.10 v2 project generator

- **File:** `SimArcade_v2.0/simarcade_v2_generator.py` (branch optimization-v2).
- A single script that writes every v2 file: backend, tools, build scripts, config, `.env.template`, `.gitignore`, the frontend (including `src/lib/api.ts`), docs and `Run_App_Dev.bat`, then prints next steps.
- **(inference)** It was produced by an AI assistant. The previous commit is named "pre-claude save", and v2 was committed the next morning.

### 5.11 Phone update portal

- **File:** `simarcade-updates/index.html`. A purple gradient page with download cards and phone instructions.

### 5.12 Content: Infiniti G35 car mod

- **File:** `drift-car-downloads/infiniti_g35_coupe_2006.zip`. **(inference)** It is hosted so the rig or other machines can download drift cars.

---

## 6. Key Design Decisions & Patterns

- **Local web UI + Python backend instead of a native GUI.** Lovable/React made the UI quick to design, and Python handles the Windows process control. The two communicate over localhost HTTP on port 51234. Source: `sim_arcade_logic.py` and `SimArcadeLauncher.tsx`.
- **Edge `--app` kiosk with a dedicated profile.** The comment in `launcher.py` says `--user-data-dir` exists "to force a new process that stays alive", so closing the window can be detected through `poll()`.
- **Config-driven paths.** `config.json` holds the `server`, `paths` and `timeouts` sections. The v0.15 banner calls this version "Config-Based", and `setup_wizard.py` generates the file. Defaults are applied if it is missing (v1). In v2, a missing file is fatal (`ConfigManager.load` raises, then `sys.exit(1)`).
- **Frozen-aware base path.** `get_base_path()` lets the same code run as a script or as a PyInstaller exe ("EXE-Ready", v0.16).
- **Process orchestration by name substring.** `psutil.process_iter` matching names case-insensitively. It is simple, but it kills **any** matching process.
- **Fail-fast start sequence with timeouts.** Each dependency (MOZA, then Meta) must appear within its timeout, or the call returns `{"status":"error"}`.
- **Hard ("nuclear") shutdown in v1:** `taskkill /F /IM msedge.exe /T` + `os._exit(0)`. v2 moves to a cooperative design: `threading.Event` with the launcher terminating its own Edge process.
- **Smart-path filenames for email deploys.** The `__` separator encodes the folder path, so files can be emailed from a phone as flat attachments. Source: `email_monitor.py` `smart_deploy_path`.
- **Secrets move out of code.** v1 hard-codes them. v2 uses environment variables (`.env.template`). Driftcade uses a `.env` file parsed by hand (`GITHUB_TOKEN`, `EMAIL_ADDRESS`, `EMAIL_PASSWORD`, `EMAIL_ALLOWED_SENDERS`), and `.env` is gitignored and protected from updates.
- **Safe-update pattern (Driftcade).** Allow-list, then backup, then stage, then validate, then deploy, then rollback on error. Backups are capped at 3. Behaviour is deny-by-default. Only one email update is processed per cycle, and processed IDs are marked to avoid retry loops.
- **Primary/fallback channels.** GitHub is the normal channel. Email is the "emergency" channel and is used only after 3 GitHub failures, at most every 5 minutes.
- **AI-assisted development.**
  - The UI comes from Lovable (`gpt-engineer-app[bot]` commits) and was remixed several times. Each remix created a new GitHub repo with a hash suffix (inference based on the suffix naming and identical root commits).
  - The v2 generator and the "pre-claude save" commit suggest the backend refactor was done with Claude (inference).
  - `simarcade-updates/index.html` addresses "Other AIs".
- **Multi-environment testing plan.** `SimArcade_v2.0/README_DEVELOPER.md` names DEV_LAPTOP (full dev), HOME_RIG (EXE testing) and SHOP_RIG (final deployment target).
- **Visual identity:** "350Z inspired" (`e510c8a`): near-black background, hot pink neon, gold, deep maroon, text glows (`text-glow-pink`, `neon-glow-pink`, `neon-glow-gold` utilities in `src/index.css`), a radial vignette and drift photography backgrounds.

---

## 7. Known Issues & Pending Roadmap

### 7.1 Security gotchas (exposed secrets / sensitive data)

- **SECURITY — Gmail app password committed in plain text.**
  - A Gmail app password for the shop's update inbox is stored in `simarcade_appv1/email_monitor.py` (constants `EMAIL_ADDRESS` / `APP_PASSWORD`) and in `simarcade_appv1/email_monitor old.py` (constants `USERNAME` / `APP_PASSWORD`).
  - It was introduced in commit `1f2a08b` and is present in `fed8072`, `563ef23` and `8a076d2`, and therefore in all later trees of main and optimization-v2.
  - The repo is on GitHub (`sredman42/simarcade_appv1`). **Action:** revoke that app password in the Google account, then purge it from history (for example with git filter-repo) or make the repo private. The v2 `tools/email_monitor.py` fixes this going forward by reading env vars.
- **SECURITY — whole Edge browser profiles committed.**
  - `simarcade_appv1/edge_profile/` (added in `a093789`) and `simarcade_appv1/SimArcade_Release/edge_profile/` (added in `68c184a`) contain `Default/Login Data`, `Login Data For Account`, `Network/Cookies`, `Web Data`, `History`, `Preferences`, extension state and more.
  - These can hold saved logins, cookies and autofill data for whatever was browsed in that kiosk profile.
  - The `.gitignore` attempts in `4e37f4a` ("ignore edge") and `78bf518` ("ignore try 2") did not untrack them. Already-tracked files stay tracked, and the second attempt added a malformed line, `- edge_profile/`. **Action:** run `git rm -r --cached edge_profile SimArcade_Release/edge_profile` and purge them from history.
- **SECURITY — unauthenticated remote code deploy (v1/v2 email monitor).**
  - **Anyone** who emails the inbox can drop files into the app folder, including `.py` files that are later executed. There is no sender whitelist, subject check or checksum (`simarcade_appv1/email_monitor.py`).
  - **(inference)** Names like `src__..__..__x` could also escape `DEPLOY_ROOT`, because `smart_deploy_path` joins the `__` parts without normalising them.
  - Driftcade's `email_updater.py` fixes this with a whitelist, a subject prefix and SHA-256.
- **SECURITY — localhost API with `Access-Control-Allow-Origin: *`** (v1) or `CORS(app)` (v2). Any web page open in a browser on the rig could POST `/app/shutdown` or `/start/vr` (inference).
- **Driftcade:**
  - `GITHUB_TOKEN` and the email credentials are read from `<root>/.env`. That file is correctly gitignored and is not in the repo.
  - The token is also sent in the `Authorization` header to `raw.githubusercontent.com` (`github_updater.py` `_download_raw_file`), which is fine. No secret is committed.

### 7.2 Bugs and fragility (from reading the code)

- **v1 `Run_App.bat` runs the app twice.** At HEAD it runs `python launcher.py` and `PAUSE` *before* the psutil auto-install block, then runs `launcher.py` again. Compare the initial version in `637fa5b`, which installed first.
- **v1 `/exit` shuts down the whole app.** `do_POST` maps both `/exit` and `/app/shutdown` to `shutdown_app()` (comment "Point BOTH…"). There is no way to end a session but keep the launcher open.
- **v1 shutdown kills every Edge window on the PC.** `taskkill /F /IM msedge.exe /T` hits the owner's personal browser as well as the kiosk window.
- **Error responses look like success.** The backend always returns HTTP 200 with `{"status":"error"}` on failure.
  - The v1 UI checks only `response.ok`, so it shows "<Action> Successful" with the error text as the description.
  - The hub `src/lib/api.ts` resolves without throwing, so the UI shows "Launching VR Mode…" even when the backend refused.
  - The hub `ApiResponse` type expects `success`, but the backend sends `status`.
  - Same in v2 `api.ts`: `response.ok` means success.
- **Process kill by substring** may kill unrelated processes whose names contain e.g. `acs.exe` (inference). v2's PID tracking is bypassed because launch keys ("moza", "meta", "cm") differ from the kill names ("MOZA Pit House.exe", …).
- **Hard-coded per-user paths.**
  - `config.json` files use `C:\Users\sredm\...` or `C:\Users\Sredm\...`.
  - `email_monitor.py` `DEPLOY_ROOT = c:\Users\Sredm\Documents\GitHub\SimArcade_AppV1`.
  - The deleted daemon refers to `C:\Users\Sredm\Desktop\SimArcade_App`.
- **Setup wizard writes `config.json` to the CWD**, not next to the exe (`CONFIG_FILE = Path("config.json")`). Launching `Setup.exe` from another directory puts the config in the wrong place (inference).
- **v1 `load_config` swallows JSON errors** (bare `except`) and silently uses defaults with an empty `paths`.
- **v2 branch is not buildable from git alone.**
  - `SimArcade_v2.0/.gitignore` contains the Python template line `lib/`, which ignores `frontend/src/lib/` (so `api.ts` is missing while `SimArcadeLauncher.tsx` imports `@/lib/api`).
  - It also contains `*.txt`, which ignores `tools/requirements.txt`, the file `build_master.bat` and the README depend on.
  - Workaround: run `simarcade_v2_generator.py` to regenerate them.
- **v2 docs mismatch.** `README_DEVELOPER.md` says `sim_arcade_logic.py` is a "Flask server", which is correct, but it lists `frontend/src/lib/` as present, which is not true in git.
- **Generated junk tracked in v1.** `build/` PyInstaller intermediates, `__pycache__/*.pyc`, three ~8.4–8.7 MB `.exe` files (no Git LFS; `.gitattributes` has only `* text=auto`), log files and empty `New Text Document*.txt` files. The `.git` directory is about 50 MB.
- **Duplicate UI sources in v1.** Both `arcade-hangout-hub-main/` and root `src/` exist, and the two `SimArcadeLauncher.tsx` files have drifted apart. Only the root `src/` is built by `Build_UI.bat`.
- **README is Lovable boilerplate** (`simarcade_appv1/README.md`, `arcade-hangout-hub*/README.md`) with `REPLACE_WITH_PROJECT_ID`.
- **Driftcade `email_updater._deploy_zip` always fails (bug).** It opens `zipfile.ZipFile(tempfile.SpooledTemporaryFile())` on an **empty** temp file before the real `io.BytesIO` extraction. That raises `BadZipFile`, which is caught and returned as "Invalid ZIP file". The leftover outer `with` line should be removed.
- **Driftcade GitHub failures are not counted.** `check_for_updates()` returns `(False, None, [])` when it cannot reach GitHub, and `run_updater.check_github()` treats that as success ("No updates available"). The 3-failure email fallback therefore triggers only on deploy failures or exceptions, not on network outages (inference from code).
- **Driftcade state files are wiped on deploy.** `github_state.json` and `email_state.json` live inside `_update_staging/`, which `UpdateManager.clear_staging()` deletes (`rmtree`) at the start of every deploy. A failed GitHub deploy loses `last_commit_sha` and forces a full-repo resync next time, and an email deploy wipes the GitHub state (inference).
- **Driftcade GitHub deploys only text files that were added or modified.**
  - `_download_raw_file` decodes the content as text, so binary files fail or are corrupted.
  - Files deleted upstream are not removed locally.
  - `stage_file` writes text in `"w"` mode, which adds Windows newline translation.
- **Driftcade rollback** restores only `ALLOWED_FOLDERS`, which is intended, but it `rmtree`s the current folder first. That is not atomic.
- **Driftcade repo name** is hard-coded as `REPO_NAME = "Driftcade"` while the GitHub repo is `sredman42/driftcade`. This works because GitHub names are case-insensitive, but it is worth noting.
- **simarcade-updates portal links are broken.** `config.json`, `setup_wizard.py`, `requirements.txt` and `backend/sim_arcade_logic.py` are not in the repo. Its link `github.com/sredman42/SimArcade-Updates` differs in case from the repo `simarcade-updates`.
- **Lovable remix sprawl.** Six hash-suffixed repos, five of them exact duplicates (three of `arcade-hangout-hub`, one of `-54a7b831`). Candidates for archiving once their history is captured here.

### 7.3 Pending roadmap (what the files say is planned or unfinished)

- **Attract Mode logic** (`arcade-hangout-hub-72afe629/src/components/attract/AttractMode.tsx`, "IMPLEMENTATION NOTES FOR LOGIC HANDOFF"):
  - carousel rotation,
  - a video interrupt every 30–45 s,
  - a VR toggle wired to the API,
  - exit wired to `shutdownApp()`,
  - responsive testing at 1080p and on the VR desktop,
  - routing the attract screen into `Index.tsx`.
- **Settings panel.** Every UI only shows a toast: "Settings locked in arcade mode." in v1 and "Opening settings panel…" in the hub. `AttractControls` has `showSettings` defaulting to false.
- **Debug mode.** `SecondaryControls` supports a `debugMode` prop, but it is always `false`.
- **SimArcade v3.0 vision** (`simarcade_v3.0/README.md`): "state machine, diagnostics, and experience system. Production kiosk software for shop sim rig."
- **Driftcade module skeleton** (empty dirs): `backend/`, `core/`, `services/`, `experiences/` (it matches the v3 "experience system", and `experiences` is an allowed update folder), `profiles/`, `config/`, `frontend/` and `tests/`. **(inference)** The plan was to port the SimArcade backend and UI into this layout with the updater in `tools/`.
- **Email daemon.** A 60 s polling daemon existed (`563ef23`) but was reverted. Driftcade's `run_updater.py` is its successor.
- **Oculus path/detection fixes.** These are referenced in `simarcade-updates/index.html`, and v2 `config.json` has an empty `meta_client`. The fixed files are not committed.
- **Multi-rig deployment:** DEV_LAPTOP → HOME_RIG → SHOP_RIG (`SimArcade_v2.0/README_DEVELOPER.md`).

---

## 8. Commit history timeline (every commit, all branches, grouped by repo)

Times are as recorded in git (Lovable commits are in UTC; Red's commits are in CST, -0600).

### simarcade_app (`/home/claude/simarcade_app`, branch main)

- `54ae8b0` 2025-12-07 12:44 -0600 — Initial commit (only `.gitattributes`).

### simarcade_appv1 (`/home/claude/simarcade_appv1`, branches main + optimization-v2)

- `637fa5b` 2025-12-07 13:05 — Initial commit: `sim_arcade_logic.py` (v0.15 Config-Based), `launcher.py`, `config.json`, `Run_App.bat`, log.
- `fadb9f9` 2025-12-07 21:14 — ".16 tested":
  - imported the Lovable UI as `arcade-hangout-hub-main/` and as the root Vite app `src/`,
  - added `Build_UI.bat`, `Build_Installer.bat`, `SimArcade.spec`, `SimArcade_Release/SimArcade.exe` and `web_ui_build/`,
  - backend v0.16 EXE-Ready.
- `a093789` 2025-12-07 23:36 — "v1.0 Stable - Fullscreen & Shutdown Fixed": backend v0.18 Nuclear Shutdown, Edge `--user-data-dir` + watch loop, wired `SimArcadeLauncher.tsx`. The `edge_profile/` folder was committed here.
- `68c184a` 2025-12-08 00:23 — "fade in save" ("good night"): UI entrance animations, `setup_wizard.py`, `Setup.spec`, `Setup.exe`, reworked `Build_Installer.bat`. `SimArcade_Release/edge_profile` was committed here.
- `1f2a08b` 2025-12-08 18:12 — "email loader": first `email_monitor.py` (hard-coded credentials) plus test payloads (`voice_test.txt`, `src/ui/*`, `ui_test_update*.py`, `email_updates/*`).
- `fed8072` 2025-12-08 22:49 — "revirt joke test": `email_monitor.py` rewritten with ZIP + smart-path deploy, old version kept as `email_monitor old.py`, multi-file test zips.
- `563ef23` 2025-12-08 23:17 — "fully working email pipe": added `email_update_daemon.py` / `_FIXED.py` (60 s poll) and deployed the joke banner `Index.tsx` to the UI.
- `8a076d2` 2025-12-08 23:59 — Revert "fully working email pipe" (removed the daemon, restored `Index.tsx`).
- `4e37f4a` 2025-12-09 10:46 — "ignore edge": `.gitignore` edits, rebuilt `web_ui_build`.
- `78bf518` 2025-12-09 11:18 — "ignore try 2": added a malformed `- edge_profile/` line to `.gitignore`.
- `9ae77dd` 2025-12-09 23:18 — "pre-claude save": rebuilt the release exes, added `sim_arcade_logic.spec` and `SimArcade_Release/sim_arcade_logic.exe`. **HEAD of main.**
- `b5c892c` 2025-12-10 11:18 — "v2 pre" (**branch optimization-v2 only**): added the `SimArcade_v2.0/` restructure (Flask backend modules, tools, build_master, frontend, docs, `.env.template`, `simarcade_v2_generator.py`).

### arcade-hangout-hub (`/home/claude/arcade-hangout-hub`; identical history in -5b3f79ce, -9bce0a60, -b0453b6e)

- `534a5a9` 2025-01-01 00:00 +0000 (Lovable) — template: new_style_vite_react_shadcn_ts.
- `24305da` 2025-12-07 04:44 +0000 (gpt-engineer-app[bot]) — Changes.
- `e510c8a` 2025-12-07 04:44 +0000 (gpt-engineer-app[bot]) — Implement 350Z inspired UI (ArcadeButton, BackgroundSlideshow, SecondaryControls, SimArcadeLauncher, drift-bg-1..3, theme).

### arcade-hangout-hub-54a7b831 and arcade-hangout-hub-a419e26a (identical histories)

- `534a5a9`, `24305da` and `e510c8a`, as above.
- `b871e91` 2025-12-09 05:29 +0000 — Changes.
- `40fae53` 2025-12-09 05:29 +0000 — Integrate backend API and status (`src/lib/api.ts`, `ConnectionStatus.tsx`, `disabled` prop, health polling).

### arcade-hangout-hub-72afe629 (`/home/claude/arcade-hangout-hub-72afe629`, newest UI)

- `534a5a9`, `24305da`, `e510c8a`, `b871e91` and `40fae53`, as above.
- `2979566` 2025-12-11 06:32 +0000 — Changes.
- `00cefc9` 2025-12-11 06:32 +0000 — Design attract mode UI scaffold (`src/components/attract/*`, CSS keyframes, tailwind fonts and shadows).
- `c82803b` 2025-12-11 06:35 +0000 — Changes.
- `ae31a4f` 2025-12-11 06:35 +0000 — Refine AttractMode visuals (richer AttractButton, Controls, MediaDisplay, Mode).

### simarcade-updates (`/home/claude/simarcade-updates`)

- `39e86fa` 2025-12-10 14:27 -0600 — Initial commit (README, `.gitattributes`).
- `dcb2798` 2025-12-10 14:41 -0600 — Create `index.html` (phone update portal).

### simarcade_v3.0 (`/home/claude/simarcade_v3.0`)

- `3f095de` 2025-12-11 21:41 -0600 — Initial commit (README with the v3 vision).

### driftcade (`/home/claude/driftcade`)

- `2a861e9` 2025-12-12 21:56 -0600 — Initial commit (Python `.gitignore`, README).
- `5bd4cff` 2025-12-12 22:26 -0600 — Initial skeleton: folder structure and gitignore.
- `5160a1e` 2025-12-13 23:31 -0600 — Add update_manager with backup and rollback logic.
- `2081c77` 2025-12-14 00:57 -0600 — Add github_updater with polling and deploy logic.
- `c155bd5` 2025-12-14 01:13 -0600 — Add email_updater fallback with sender whitelist and checksum.
- `b54232a` 2025-12-14 01:23 -0600 — Add run_updater controller with GitHub primary and email fallback.

### drift-car-downloads (`/home/claude/drift-car-downloads`)

- `acdb341` 2026-01-26 20:19 -0600 — Create `infiniti_g35_coupe_2006.zip` (Assetto Corsa car mod, about 94.6 MB).
