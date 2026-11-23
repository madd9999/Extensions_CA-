# CA Office pyRevit Extension

Generic pyRevit tools for the office. This whole repository is **one** pyRevit extension.

| Tab > Panel > Button | What it does |
|---|---|
| **Childers > Fun > Drop Image** | Drops an image down the screen. |

## Install (one time, about 1 minute)

1. Close Revit.
2. Press the **Windows key**, type `cmd`, press **Enter**.
3. Paste this line and press **Enter**:

   ```
   pyrevit extend ui CAOffice https://github.com/madd9999/Extensions_CA-.git
   ```

4. Open Revit – the **Childers** tab is there.

If you previously installed this from a ZIP: remove that folder from
**pyRevit > Settings > Custom Extension Directories** so the buttons don't show twice.

## Update

In Revit click **pyRevit tab > Update** (or run `pyrevit extensions update CAOffice` in cmd),
then **Reload**.

## Uninstall

```
pyrevit extensions delete CAOffice
```

## For the maintainer

Folder layout must stay `<Name>.tab\<Name>.panel\<Name>.pushbutton\script.py` at the root of the repo.
New generic tools = new panels/buttons inside `Childers.tab` (or another `.tab` folder at the root).
