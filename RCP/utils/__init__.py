# Copyright (c) 2026 Benedikt Singer (benedikt.singer@epfl.ch)
# Refactored with the assistance of Claude Opus 4.6 by Anthropic (https://www.anthropic.com)
# Licensed under the MIT License. See LICENSE file in the project root.

"""Standalone result parsers for structure prediction and sequence design tools.

Each parser takes a root directory and returns a pandas DataFrame with
design IDs and associated metrics. They are independent of the pipeline
manager and can be used directly from a Jupyter notebook.

Usage:
    from utils.result_parsers import (
        parse_af3_results,
        parse_chai_results,
        parse_boltz_results,
        parse_ligandmpnn_results,
        parse_carbonara_results,
        parse_rfd3_results,
        merge_results,
    )

    af3_df = parse_af3_results("/path/to/af3_outputs")
"""

from .result_parsers import (
    parse_af3_results,
    parse_chai_results,
    parse_boltz_results,
    parse_ligandmpnn_results,
    parse_carbonara_results,
    parse_rfd3_results,
    merge_results,
)

__all__ = [
    "parse_af3_results",
    "parse_chai_results",
    "parse_boltz_results",
    "parse_ligandmpnn_results",
    "parse_carbonara_results",
    "parse_rfd3_results",
    "merge_results",
]
