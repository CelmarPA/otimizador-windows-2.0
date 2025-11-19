# benchmarks.py
import math
import os
import threading
import time
import shutil
import tempfile

# Optional libs
try:
    import numpy as np
    _HAS_NUMPY = True
except Exception:
    _HAS_NUMPY = False

try:
    import glfw
    import OpenGL.GL as gl
    _HAS_GL = True
except Exception:
    _HAS_GL = False


#  Helpers
def _safe_log(log_panel, msg):
    if log_panel:
        try:
            log_panel.log(msg)
        except Exception:
            pass

    else:
        print(msg)


def _normalize(value, ref_min, ref_max) -> float:
    """Map value in [ref_min, ref_max] -> [0,10] (clamped)."""
    if value <= ref_min:
        return 0.0
    if value >= ref_max:
        return 10.0

    # linear mapping
    return round((value - ref_min) / (ref_max - ref_min) * 10.0, 2)


# ---------- GPU benchmark (OpenGL FPS) ----------
def run_gpu_benchmark(duration: float=5.0, log_panel: None=None) -> tuple[float, str]:
    """
    Runs a REAL GPU benchmark measuring rendering FPS using OpenGL.
    Returns a score of 0–10.
    """
    _safe_log(log_panel, "▶️ GPU: starting OpenGL benchmark...")

    if not _HAS_GL:
        return 0.0, "missing glfw / PyOpenGL"

    try:
        if not glfw.init():
            return 0.0, "glfw.init failed"

        # Hidden window
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(1024, 768, "GPU Benchmark", None, None)

        if not window:
            glfw.terminate()
            return 0.0, "create_window failed"

        glfw.make_context_current(window)

        frames = 0
        start = time.time()

        while time.time() - start < duration:
            # Animated sine wave — heavily loads the GPU pipeline
            t = time.time() - start
            r = (math.sin(t * 3) - 1) / 2

            gl.glClearColor(r * 0.6, 0.2 + 0.1 * r, 1 - r * 0.6, 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            # small CPU work to keep loop realistic
            _ = math.sin(t) * math.cos(t)
            glfw.swap_buffers(window)
            glfw.poll_events()

            frames += 1

        end = time.time()
        glfw.terminate()

        fps = frames / (end - start)

        # reference: 200 FPS -> 10. 20 FPS -> ~1

        score = _normalize(fps, ref_min=10, ref_max=200)

        return score, f"{round(fps,2)} FPS"

    except Exception as e:
        try: glfw.terminate()
        except Exception:
            pass
        return 0.0, f"error: {e}"

# ---------- CPU benchmark ---------
def run_cpu_benchmark(iter_mult: int = 1, log_panel: None=None) -> tuple[float, str]:
    """
    CPU benchmark: uses numpy matrix multiply (if available) or a fallback integer loop.
    Returns score 0-10 and a detail string (ops/sec or duration).
    """
    _safe_log(log_panel, "▶️ CPU: starting synthetic benchmark...")

    # Realistic references for 0-10 scale
    REF_MIN = 50 # Low-end PC
    REF_MAX = 700 # Top of the market (7950X, 13900K)

    if _HAS_NUMPY:
        n = 1000 * iter_mult  # matrix size. adjust per machine
        # limit memory: ensure n isn't insane
        if n > 3000:
            n = 3000

        try:
            a = np.random.rand(n, n).astype(np.float32)
            b = np.random.rand(n, n).astype(np.float32)

            start = time.time()
            _ = a.dot(b)
            duration = time.time() - start

            # approximate FLOPS for matmul ~ 2*n^3 operations
            flops = 2.0 * (n ** 3)
            gflops = flops / (duration * 1e9)

            # Scientific standardization
            score = _normalize(gflops, ref_min=REF_MIN, ref_max=REF_MAX)

            return score, f"{gflops:.2f} GFLOPS (time {duration:.2f}s)"

        except MemoryError:
            return 0.0, "MemoryError"
        except Exception as e:
            return 0.0, f"CPU error: {e}"

    # Fallback (no numpy): CPU-bound hashing loop
    try:
        import hashlib
        iters = 200_000
        start = time.time()
        s = b"benchmark"

        for i in range(iters):
            hashlib.sha256(s + str(i).encode()).digest()

        duration = time.time() - start

        # map duration to score: faster -> higher
        score = _normalize(1.0 / max(duration, 0.0001), ref_min=0.01, ref_max=1.0)

        return score, f"hash loop {iters} iters in {duration:.2f}s"

    except Exception as e:
        return 0.0, f"error: {e}"


# ---------- RAM benchmark ----------
def run_ram_benchmark(size_mb: int = 1024, log_panel: None=None) -> tuple[float, str]:
    """
    Allocate buffers and measure sequential memory read/write bandwidth.
    Returns score 0-10 and detail string.
    """

    _safe_log(log_panel, f"▶️ RAM: testing {size_mb} MB allocation...")

    if not _HAS_NUMPY:
        # fallback: try to allocate a large bytearray
        try:
            start = time.time()
            b = bytearray(size_mb * 1024 * 1024)

            # Write pattern
            for i in range(0, len(b), 4096):
                b[i] = (i % 256)

            # Read sum
            s = 0
            for i in range(0, len(b), 4096):
                s += b[i]

            duration = time.time() - start
            mbps = size_mb / duration
            score = _normalize(mbps, ref_min=500.0, ref_max=70000.0) # range tuned generously

            return score, f"{mbps:.2f} MB/s ({duration:.2f}s)"

        except MemoryError:
            return 0.0, "MemoryError"
        except Exception as e:
            return 0.0, f"error: {e}"

    try:
        # use numpy for faster and realistic memory ops
        arr = np.random.randint(0, 255, size=(size_mb * 256,), dtype=np.uint8)  # ~size_mb MB
        start = time.time()

        # sequential write (set)
        arr[:] = 123
        # sequential read (sum)
        _ = arr.sum()

        duration = time.time() - start
        mbps = size_mb / duration

        score = _normalize(mbps, ref_min=500.0, ref_max=70000.0)

        return score, f"{mbps:.2f} MB/s ({duration:.2f}s)"

    except MemoryError:
        return 0.0, "MemoryError"
    except Exception as e:
        return 0.0, f"error: {e}"


# ---------- Disk benchmark ----------
def run_disk_benchmark(size_mb: int = 500, log_panel: None=None) -> tuple[float, str]:
    """
    Sequential write/read and a small random read test.
    Returns score 0-10 and detail string.
    """
    _safe_log(log_panel, f"▶️ DISK: testing {size_mb} MB sequential write/read...")

    tmp_dir = tempfile.mkdtemp()
    file_path = os.path.join(tmp_dir, "disk_test.bin")

    try:
        block = os.urandom(1024 * 1024)  # 1MB block

        # Write
        start = time.time()

        with open(file_path, "wb") as f:
            for _ in range(size_mb):
                f.write(block)

            f.flush()
            os.fsync(f.fileno())

        write_time = time.time() - start
        write_mb_s = size_mb / write_time if write_time > 0 else 0.0
        _safe_log(log_panel, f"DISK write: {write_mb_s:.2f} MB/s ({write_time:.2f}s)")

        # Read sequential
        start = time.time()

        with open(file_path, "rb") as f:
            while f.read(1024 * 1024):
                pass

        read_time = time.time() - start
        read_mb_s = size_mb / read_time if read_time > 0 else 0.0
        _safe_log(log_panel, f"DISK read: {read_mb_s:.2f} MB/s ({read_time:.2f}s)")

        # small random reads (10 x 4MB)
        import random

        rand_reads = 10
        rand_block = 4
        start = time.time()

        with open(file_path, "rb") as f:
            for _ in range(rand_reads):
                pos = random.randint(0, max(0, size_mb - rand_block)) * 1204 * 1024
                f.seek(pos)
                f.read(rand_block * 1024 * 1024)

        rand_time = time.time() - start
        rand_mb_s = (rand_reads * rand_block) / rand_time if rand_time > 0 else 0.0
        _safe_log(log_panel, f"DISK random read: {rand_mb_s:.2f} MB/s ({rand_time:.2f}s)")

        # normalize using read/write averages (tune refs per expectations)
        metric = (write_mb_s * 0.5) + (read_mb_s * 0.4) + (rand_mb_s * 0.1)

        score = _normalize(metric, ref_min=20.0, ref_max=2000.0)
        detail = f"seq_write={write_mb_s:.2f}MB/s seq_read={read_mb_s:.2f}MB/s rand_read={rand_mb_s:.2f}MB/s"

        return score, detail

    except Exception as e:
        return 0.0, f"error: {e}"

    finally:
        try:
            shutil.rmtree(tmp_dir)
        except Exception:
            pass


# ---------- High-level runner ----------
class PerformanceTester():

    def __init__(self, log_panel=None, gpu_duration: float = 5.0) -> None:
        self.log_panel = log_panel
        self.gpu_duration = gpu_duration

    def _log(self, msg) -> None:
        if self.log_panel:
            _safe_log(self.log_panel, msg)
        else:
            print(msg)

    def run_all(self, async_run: bool = False):
        """
        Runs CPU, RAM, Disk, GPU. If async_run True => runs in a background thread and returns immediately.
        Otherwise, blocks and returns a results dict.
        """

        if async_run:
            thread = threading.Thread(target=self.run_all_internal, daemon=True)
            thread.start()
            print(thread)
            return thread

        else:
            return self.run_all_internal()

    def run_all_internal(self) -> dict:
        self._log("▶️ Starting full hardware benchmark suite...")

        # CPU
        cpu_score, cpu_detail = run_cpu_benchmark(log_panel=self.log_panel)
        self._log(f"🖥 CPU Score: {cpu_score}/10  — {cpu_detail}")

        # RAM
        ram_score, ram_detail = run_ram_benchmark(log_panel=self.log_panel)
        self._log(f"💾 RAM Score: {ram_score}/10 — {ram_detail}")

        # Disk
        disk_score, disk_detail = run_disk_benchmark(log_panel=self.log_panel)
        self._log(f"🗄 Disk Score: {disk_score}/10 — {disk_detail}")

        # GPU
        gpu_score, gpu_detail = run_gpu_benchmark(duration= self.gpu_duration, log_panel=self.log_panel)
        self._log(f"🎮 GPU Score: {gpu_score}/10 — {gpu_detail}")

        # Final weighted score
        # Weights: CPU 30%, RAM 20%, Disk 20%, GPU 30%
        final = round(cpu_score * 0.30 + ram_score * 0.20 + disk_score * 0.20 + gpu_score * 0.30, 2)
        self._log(f"🏆 Final Score: {final}/10")

        return {
            "CPU": (cpu_score, cpu_detail),
            "RAM": (ram_score, ram_detail),
            "Disk": (disk_score, disk_detail),
            "GPU": (gpu_score, gpu_detail),
            "Final": final
        }


# If run directly
if __name__ == "__main__":
    tester = PerformanceTester()
    res = tester.run_all()
    print(res)
