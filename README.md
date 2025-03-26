<div align="center">
  <img src="logo.jpg" alt="Logo" width="200">
  <h2>Assault Cube Multicheat</h2>
  <p>A trainer for Assault Cube written in Python.</p>
</div>

## Features

- [x] ESP
- [x] Aimbot (experimental)
- [x] Jump higher
- [ ] God mode

## Building

With Python 3.11+ installed on Windows, install [pyMeow], then install the dependencies
with:

```powershell
pip install .\pyMeow-1.73.42.zip
pip install -r requirements.txt
```

Then, build the project with:

```powershell
.\scripts\build.ps1
```

The first time, make sure to say yes to [Nuitka]'s prompts to install its dependencies.

## Developing

Follow the same steps as building, but instead of running the build script, run Python:

```powershell
python .\src\main.py
```

[pyMeow]: https://github.com/qb-0/PyMeow?tab=readme-ov-file#floppy_disk-installation
[Nuitka]: https://nuitka.net/
