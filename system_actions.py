import shutil
import webbrowser
import os
import subprocess
import threading
from datetime import datetime
from performance_tester import PerformanceTester
from tkinter import messagebox



def auto_log(func):
    def wrapper(self, *args, **kwargs):
        if hasattr(self, "log_panel") and self.log_panel:
            self.log_panel.info(f"▶️ [{datetime.now().strftime('%H:%M:%S')}] Starting: {func.__name__}")

        try:
            result = func(self, *args, **kwargs)

            if hasattr(self, "log_panel") and self.log_panel:
                self.log_panel.success(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Finished: {func.__name__}")

            return result

        except Exception as e:
            if hasattr(self, "log_panel") and self.log_panel:
                self.log_panel.error(f"❌ Error in {func.__name__}: {e}")
            raise e

    return wrapper


class SystemActions:

    def __init__(self, log_panel=None) -> None:
        self.log_panel = log_panel
        self.bench = PerformanceTester(log_panel=log_panel)

    @auto_log
    def create_restore_point(self) -> None:
        description = "Before Optimization"
        self.log_panel.info("Starting restore point creation...")

        cmd = [
            "powershell",
            "-Command",
            f'Checkpoint-Computer -Description "{description}" -RestorePointType "Modify_Settings"'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        self.log_panel.success("Restore point created successfully!")

    @auto_log
    def pc_performance_test(self):
        self.bench.run_all(async_run=True)

    @auto_log
    def enable_disable_sysmain(self) -> None:
        """
        Toggle SysMain (user-friendly + non-blocking + safe):
        - If running → ask to disable
        - If stopped → ask to enable
        """
        # Check current state
        try:
            result = subprocess.run(
                'powershell -Command "(Get-Service -Name SysMain).Status"',
                capture_output=True, text=True, shell=True
            )

            status = result.stdout.strip().lower()

        except Exception as e:
            self.log_panel.error(f"❌ Error checking SysMain state: {e}")
            return

        # Ask user confirmation



        if status.lower() == "running":
            action = "disable"
            ask_title = "Disable SysMain"
            ask_message = "SysMain is ACTIVE. Do you want to deactivate it?"

        else:
            action = "enable"
            ask_title = "Enable SysMain"
            ask_message = "SysMain is DISABLED. Do you want to enable it?"

        answer = messagebox.askyesno(ask_title, ask_message)

        if not answer:
            self.log_panel.info("Operation canceled by the user.")
            return

        # Run in background
        def worker_toggle() -> None:
            """Background task — prevents UI freeze"""

            try:
                if action == "disable":
                    cmd = (
                        'powershell -Command '
                        '"Stop-Service SysMain -Force; '
                        ' Set-Service SysMain -StartupType Disabled"'
                    )

                else:
                    cmd = (
                        'powershell -Command '
                        '"Set-Service SysMain -StartupType Automatic; '
                        ' Start-Service SysMain"'
                    )

                proc = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True
                )

                if proc.returncode != 0:
                    self.log_panel.error(
                        f"❌ Error executing SysMain ({action}): {proc.stderr.strip()}"
                    )
                    return

                # Verify the result
                verify = subprocess.run(
                    'powershell -Command "(Get-Service -Name SysMain).Status"',
                    capture_output=True, text=True, shell=True
                )

                new_status = verify.stdout.strip().lower()

                if action == "disable" and new_status == "stopped":
                    self.log_panel.success("✅ SysMain was successfully DISABLED!")

                elif action == "enable" and new_status == "running":
                    self.log_panel.success("✅ SysMain was successfully activated!")

                else:
                    self.log_panel.error("⚠️ Command executed, but the final state does not match.")

            except Exception as e:
                self.log_panel.error(f"❌ Exception during SysMain toggle: {e}")

        # Start background thread
        threading.Thread(target=worker_toggle, daemon=True).start()

    @auto_log
    def clean_temporary_files(self) -> None:

        # Safe directories to clean
        temp_dirs = [
            os.path.expandvars(r"%TEMP%"),
            r"C:\Windows\Temp",
            r"C:\Windows\Prefetch",
        ]

        total_deleted, total_errors = 0, 0

        self.log_panel.info("🧹 Starting safe cleaning of temporary files...")

        for directory in temp_dirs:
            path = os.path.abspath(directory)

            # Check if it exists
            if not os.path.exists(path):
                self.log_panel.warning(f"Directory does not exist: {path}")
                continue

            self.log_panel.info(f"📁 Clearing: {path}")

            # Iterates through all files and folders within the directory
            for root, dirs, files in os.walk(path):
                # Delete files
                for file in files:
                    file_path = os.path.join(root, file)

                    try:
                        os.remove(file_path)
                        total_deleted += 1

                    except PermissionError:
                        total_errors += 1
                        self.log_panel.warning(f"🔒 File in use (not removed): {file_path}")

                    except Exception as e:
                        total_errors += 1
                        self.log_panel.error(f"Error removing file {file_path}: {e}")

                # Delete empty folders
                for folder in dirs:
                    folder_path = os.path.join(root, folder)

                    try:
                        shutil.rmtree(folder_path, ignore_errors=True)

                    except Exception as e:
                        total_errors += 1
                        self.log_panel.warning(f"Could not remove folder {folder_path}: {e}")

        self.log_panel.success(f"🧽 Files removed: {total_deleted}")
        if total_errors > 0:
            self.log_panel.warning(f"⚠️ Problems found: {total_errors} items could not be removed")

        if total_deleted == 0:
            raise RuntimeError("No temporary files could be cleaned. There may be insufficient permissions.")

    @auto_log
    def deep_system_cleanup(self) -> None:
        """
        PRO Cleaning:
        - WinSxS Cleanup (Component Store) via DISM
        - Delivery Optimization
        - Windows Update Cache
        - System logs
        """

        #1. WinSxS Cleanup (Secure via DISM)
        print("OK")
        try:
            self.log_panel.info("🧹 Clearing WinSxS (Component Store)...")
            cmd = 'Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                self.log_panel.success("✔ WinSxS cleaned successfully!")

            else:
                self.log_panel.warning(f"⚠️ WinSxS returned messages:\n{result.stderr}")

        except Exception as e:
            self.log_panel.error(f"Error WinSxS Cleanup: {e}")

        # Delivery Optimization Cache
        try:
            self.log_panel.info("📦 Clearing Delivery Optimization Cache...")

            subprocess.run(
                'powershell -command "Remove-Item -Path \\"C:\\ProgramData\\Microsoft\\Windows\\DeliveryOptimization\\*"\\" -Recurse -Force -ErrorAction SilentlyContinue"',
                shell=True
            )

            self.log_panel.success("✔ Delivery Optimization clean!")

        except Exception as e:
            self.log_panel.error(f"Error Delivery Optimization: {e}")

        # Windows Update Cache
        try:
            self.log_panel.info("🔄 Clearing Windows Update Cache...")

            # Stop services to free up folder
            subprocess.run('net stop wuauserv', shell=True)
            subprocess.run('net stop bits', shell=True)

            shutil.rmtree(r"C:\Windows\SoftwareDistribution", ignore_errors=True)

            # Recreate directory
            os.makedirs(r"C:\Windows\SoftwareDistribution", exist_ok=True)

            # Restart services
            subprocess.run('net start wuauserv', shell=True)
            subprocess.run('net start bits', shell=True)

            self.log_panel.success("✔ Windows Update Cache clear!")

        except Exception as e:
            self.log_panel.error(f"Error clearing Windows Update Cache: {e}")

        # System Logs Cleanup
        try:
            self.log_panel.info("🗒 Clearing system logs...")

            log_paths = [
                r"C:\Windows\Logs",
                r"C:\Windows\System32\LogFiles",
                r"C:\Windows\Temp",
            ]

            for path in log_paths:
                try:
                    shutil.rmtree(path, ignore_errors=True)
                    os.makedirs(path, exist_ok=True)
                    self.log_panel.info(f"✔ Clear logs: {path}")

                except Exception as e:
                    self.log_panel.warning(f"⚠️ Could not clear {path}: {e}")

            self.log_panel.success("✔ System logs cleared!")

        except Exception as e:
            self.log_panel.error(f"Error Logs: {e}")

        # Final
        self.log_panel.success("🎉 Deep cleaning completed successfully!")


    @auto_log
    def enable_high_power_plan(self) -> None:
        cmd = 'powershell -Command "powercfg -setactive SCHEME_MIN"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

    @auto_log
    def disable_background_apps(self) -> None:
        cmd = (
            'powershell -Command "Set-ItemProperty HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\'
            'BackgroundAccessApplications GlobalUserDisabled 1"'
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

    @auto_log
    def complete_optimization(self) -> None:
        self.log_panel.info("Running complete optimization…")
        # TODO: implementar otimizações reais

    @auto_log
    def update_software(self) -> None:
        self.log_panel.info("Updating all software…")
        # TODO: implementar atualização real

    @auto_log
    def massgrave_activator(self) -> None:
        try:
            webbrowser.open("https://massgrave.dev/")
        except Exception as e:
            raise RuntimeError(f"Erro ao abrir o site: {e}")

    def start_cleanup(self) -> None:
        #  Initial log
        if self.log_panel:
            self.log_panel.info("🧽 Starting deep system cleanup...")

        def run():
            try:
                self.deep_system_cleanup()

            except Exception as e:
                if self.log_panel:
                    self.log_panel.error(f"Error deep system cleanup: {e}")

        # Executes in a thread
        threading.Thread(target=run, daemon=True).start()