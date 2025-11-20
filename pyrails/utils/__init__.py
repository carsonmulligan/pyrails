"""Utility functions for PyRails."""
from .inflector import camelize, classify, pluralize, singularize, tableize, underscore
from .prompts import confirm, prompt_text, select_option

__all__ = [
    "camelize",
    "classify",
    "pluralize",
    "singularize",
    "tableize",
    "underscore",
    "confirm",
    "prompt_text",
    "select_option",
]
