from pathlib import Path
from functools import lru_cache
import yaml, os

CONFIG_PATH = Path("config/settings.yaml")

# Allow enviroment overrides
def _merge_env(cfg):
    mapping = {
        "model_name": ("SCRAPER_MODEL_NAME", str),
        "api_key": ("SCRAPER_API_KEY", str),
        "max_workers": ("SCRAPER_MAX_WORKERS", int),
        "output_dir": ("SCRAPER_OUTPUT_DIR", str)
    }
    for key, (env, caster) in mapping.items():
        v = os.getenv(env)
        if v is not None:
            cfg[key] = caster(v)      
    return cfg

@lru_cache(maxsize=1)
def get_config(path: str | Path = CONFIG_PATH) -> dict:
    with open(path, 'r') as f:
        cfg = yaml.safe_load(f) or {}
    return _merge_env(cfg)