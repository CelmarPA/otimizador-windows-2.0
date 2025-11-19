import shutil
import webbrowser
import os
import subprocess
from datetime import datetime
from performance_tester import PerformanceTester


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
    def disable_sysmain(self) -> None:
        cmd = 'powershell -Command "Stop-Service SysMain; Set-Service SysMain -StartupType Disabled"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

    @auto_log
    def clean_temporary_files(self) -> None:
        temp_dirs = [r"%TEMP%", r"C:\Windows\Temp"]
        for directory in temp_dirs:
            path = os.path.expandvars(directory)
            try:
                shutil.rmtree(path, ignore_errors=False)
            except Exception as e:
                raise RuntimeError(f"Erro ao limpar {path}: {e}")

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
