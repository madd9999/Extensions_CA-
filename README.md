# Office pyRevit Extensions

pyRevit extensions for the office. Each `*.extension` folder in this repository is one extension.

| Extension | What it does |
|---|---|
| `FallingImage.extension` | **Childers > Fun > Drop Image** – drops an image down the screen. |

## Install (one time)

1. Pick a folder for the extensions, e.g. `C:\pyRevit\OfficeExtensions`.
2. Get the files into it, using either option:
   - **With git:** `git clone <repo URL> "C:\pyRevit\OfficeExtensions"`
   - **Without git:** on the GitHub page click **Code > Download ZIP**, then unzip it into that folder.
3. In Revit go to **pyRevit tab > Settings > Custom Extension Directories**, click **Add folder**,
   pick that folder, then **Save Settings and Reload**.

The new tab and buttons appear after the reload.

## Update

- **With git:** run `git pull` inside the folder, then click **pyRevit > Reload** in Revit.
- **Without git:** download the ZIP again, replace the folder contents, then click Reload.
