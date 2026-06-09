"""
╔══════════════════════════════════════════════════════════════╗
║   Desktop Shortcut Creator for EV PowerShare App            ║
║   Run once:  python create_shortcut.py                      ║
║   Works on:  Windows | macOS | Linux                        ║
╚══════════════════════════════════════════════════════════════╝
"""
 
import os
import sys
import stat
 
# ── Path to the main app  ─────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE   = os.path.join(SCRIPT_DIR, "home_energy_app.py")
PYTHON_EXE = sys.executable          
 
 
def create_windows_shortcut():
    """Creates a .bat launcher + a .lnk shortcut on the Desktop."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
 
    # ── 1. Write a .bat launcher ──────────────────────────────
    bat_path = os.path.join(SCRIPT_DIR, "EV_PowerShare.bat")
    bat_content = f'@echo off\n"{PYTHON_EXE}" "{APP_FILE}"\n'
    with open(bat_path, "w") as f:
        f.write(bat_content)
 
    # ── 2. Try to create a proper .lnk via PowerShell ─────────
    lnk_path = os.path.join(desktop, "EV PowerShare.lnk")
    ps_cmd = (
        f'$s=(New-Object -COM WScript.Shell).CreateShortcut("{lnk_path}");'
        f'$s.TargetPath="{PYTHON_EXE}";'
        f'$s.Arguments=\'"{APP_FILE}"\';'
        f'$s.WorkingDirectory="{SCRIPT_DIR}";'
        f'$s.Description="EV PowerShare Energy Dashboard";'
        f'$s.Save()'
    )
    ret = os.system(f'powershell -Command "{ps_cmd}"')
 
    if ret == 0 and os.path.exists(lnk_path):
        print(f"[OK] Windows shortcut created:\n     {lnk_path}")
    else:
        # Fallback: copy the .bat to the Desktop
        import shutil
        bat_desktop = os.path.join(desktop, "EV_PowerShare.bat")
        shutil.copy(bat_path, bat_desktop)
        print(f"[OK] Launcher copied to Desktop:\n     {bat_desktop}")
        print("     (double-click it to launch the app)")
 
 
def create_macos_shortcut():
    """Creates a double-clickable .command script on the Desktop."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    cmd_path = os.path.join(desktop, "EV PowerShare.command")
 
    content = f"""#!/bin/bash
# EV PowerShare – Energy Dashboard launcher
cd "{SCRIPT_DIR}"
"{PYTHON_EXE}" "{APP_FILE}"
"""
    with open(cmd_path, "w") as f:
        f.write(content)
 
    # Make it executable
    st = os.stat(cmd_path)
    os.chmod(cmd_path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
 
    print(f"[OK] macOS launcher created:\n     {cmd_path}")
    print("     Double-click it in Finder to open the app.")
    print("     (If blocked by Gatekeeper: right-click → Open)")
 
 
def create_linux_shortcut():
    """Creates a .desktop file on the Desktop (follows freedesktop spec)."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    os.makedirs(desktop, exist_ok=True)
 
    desktop_path = os.path.join(desktop, "ev-powershare.desktop")
    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=EV PowerShare
Comment=Smart Energy Management Dashboard
Exec={PYTHON_EXE} {APP_FILE}
Path={SCRIPT_DIR}
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;Science;
"""
    with open(desktop_path, "w") as f:
        f.write(content)
 
    # Mark as executable (required by most Linux DEs)
    st = os.stat(desktop_path)
    os.chmod(desktop_path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
 
    print(f"[OK] Linux .desktop shortcut created:\n     {desktop_path}")
    print("     Right-click it → 'Allow Launching' if prompted.")
 
 
# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 52)
    print(" 🔋 EV PowerShare – Desktop Shortcut Creator")
    print("=" * 52)
 
    if not os.path.exists(APP_FILE):
        print(f"[ERROR] App file not found:\n  {APP_FILE}")
      
        sys.exit(1)
 
    platform = sys.platform
 
    if platform.startswith("win"):
        create_windows_shortcut()
    elif platform == "darwin":
        create_macos_shortcut()
    else:
        create_linux_shortcut()
 
    print()
    print("Done! Your desktop shortcut is ready.")
    print("=" * 52)
 