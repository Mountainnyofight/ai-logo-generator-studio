"""Diffusion kernel. Thin wrapper over diffusers, device-aware, lazy-loaded."""
from __future__ import annotations

import logging

log = logging.getLogger("logo_kernels.diffusion")

class DiffusionKernel:
    def __init__(self, device: str = "cuda") -> None:
        self.device = device
        self._pipe = None

    def _ensure_pipe(self):
        if self._pipe is not None:
            return
        from diffusers import AutoPipelineForText2Image  # type: ignore
        import torch  # type: ignore
        dev = self.device if torch.cuda.is_available() or self.device == "cpu" else "cpu"
        self._pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float16 if dev == "cuda" else torch.float32,
        ).to(dev)
        log.info("diffusion pipe ready on %s", dev)

    def sample(self, prompt: str, steps: int = 28, size: tuple[int, int] = (1024, 1024)):
        self._ensure_pipe()
        assert self._pipe is not None
        return self._pipe(prompt=prompt, num_inference_steps=steps,
                          height=size[1], width=size[0]).images[0]