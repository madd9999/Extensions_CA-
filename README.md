# Office pyRevit Extensions

pyRevit extensions for the office. Each `*.extension` folder in this repository is one extension.

| Extension | What it does |
|---|---|
| `FallingImage.extension` | **Childers > Fun > Drop Image** – drops an image down the screen. |

## Install (one time)

1. Pick a folder for the extensions, e.g. `C:\pyRevit\OfficeExtensions`.
2. Get the files into it, using either option:
   - **With git:** `git clone https://github.com/madd9999/Extensions_CA-.git "C:\pyRevit\OfficeExtensions"`
   - **Without git:** on the GitHub page click **Code > Download ZIP**, then unzip it into that folder.
   > **ZIP users – check the folders.** The ZIP unzips into extra folders like
   > `Extensions_CA--main\Extensions_CA--main\`. pyRevit only sees `*.extension` folders that sit
   > **directly** inside the folder you add. Open the folders until you see `FallingImage.extension`,
   > then either move everything from there up into `C:\pyRevit\OfficeExtensions`, or add that inner
   > folder in step 3.
   >
   > Correct: `C:\pyRevit\OfficeExtensions\FallingImage.extension\Childers.tab\...`
3. In Revit go to **pyRevit tab > Settings > Custom Extension Directories**, click **Add folder**,
   pick the folder that directly contains the `*.extension` folders, then **Save Settings and Reload**.

The new tab and buttons appear after the reload.

## Update

- **With git:** run `git pull` inside the folder, then click **pyRevit > Reload** in Revit.
- **Without git:** download the ZIP again, replace the folder contents, then click Reload.
