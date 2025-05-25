"""
bot/plugins/__init__.py

Initializer for all plugin modules in the 'plugins' folder.
Ensures plugin discovery when using dynamic import or auto-loader.

Structure-compliant with 36-point bot architecture.
"""

import os
import importlib

# This ensures that all plugins in this directory get imported automatically
def load_plugins():
    plugin_folder = os.path.dirname(__file__)
    for file in os.listdir(plugin_folder):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"bot.plugins.{file[:-3]}"
            try:
                importlib.import_module(module_name)
                print(f"[PLUGIN] Loaded: {module_name}")
            except Exception as e:
                print(f"[PLUGIN ERROR] Failed to load {module_name}: {e}")

# Automatically load all plugins when this module is imported
load_plugins()
