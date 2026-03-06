# Copyright (c) 2026 Benedikt Singer (benedikt.singer@epfl.ch)
# Refactored with the assistance of Claude Opus 4.6 by Anthropic (https://www.anthropic.com)
# Licensed under the MIT License. See LICENSE file in the project root.

"""Standalone result parsers for structure prediction and sequence design tools.

Each function takes a root directory path and returns a pandas DataFrame.
No pipeline or cluster configuration is needed — just point at the directory
where results were rsynced to.
"""

import gzip
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# AlphaFold3
# ---------------------------------------------------------------------------

def parse_af3_results(af3_dir: str) -> pd.DataFrame:
    """Parse AlphaFold3 outputs into per-prediction records.

    Supports multiple directory layouts:

    1. Nested (original)::

        af3_dir/
          <sample_batch>/
            <seq_id>/
              <job_name>/
                seed-<S>_sample-<N>/
                  <prefix>_summary_confidences.json
                  <prefix>_confidences.json
                  <prefix>_model.cif

    2. Flat / alternative nesting — any ``*_summary_confidences.json``
       found recursively is parsed. Seed/sample are extracted from the
       parent directory name when possible.

    Returns a DataFrame with columns:
        id, seed, af3_sample, ptm, iptm, ranking_score,
        atom_plddts, pae, chain_pair_pae_min, fraction_disordered,
        has_clash, model_path
    """
    af3_path = Path(af3_dir)
    records: list[dict] = []

    for summary_file in sorted(af3_path.rglob("*_summary_confidences.json")):
        # Try to extract seed/sample from parent dir name
        seed_sample_match = re.match(
            r"seed-(\d+)_sample-(\d+)", summary_file.parent.name)
        if seed_sample_match:
            seed = int(seed_sample_match.group(1))
            af3_sample = int(seed_sample_match.group(2))
            # seq_id is two levels above the seed-sample dir, but AF3
            # sometimes adds an extra "output/" level:
            #   <seq_id>/<job_name>/seed-*/...           → parent^3 = seq_id
            #   <seq_id>/output/<job_name>/seed-*/...    → parent^3 = "output"
            seq_id = summary_file.parent.parent.parent.name
            if seq_id == "output":
                seq_id = summary_file.parent.parent.parent.parent.name
        else:
            seed = 0
            af3_sample = 0
            # Use the immediate parent directory as seq_id
            seq_id = summary_file.parent.name

        with open(summary_file) as f:
            summary = json.load(f)

        prefix = summary_file.name.replace("_summary_confidences.json", "")
        conf_file = summary_file.parent / f"{prefix}_confidences.json"
        mean_plddt = np.nan
        mean_pae = np.nan
        if conf_file.exists():
            with open(conf_file) as f:
                conf = json.load(f)
            if "atom_plddts" in conf:
                mean_plddt = float(np.mean(conf["atom_plddts"]))
            if "pae" in conf:
                mean_pae = float(np.mean(conf["pae"]))

        def _safe_mean(val):
            return float(np.mean(val)) if val is not None else np.nan

        records.append({
            "id": seq_id,
            "seed": seed,
            "af3_sample": af3_sample,
            "ptm": _safe_mean(summary.get("ptm")),
            "iptm": _safe_mean(summary.get("iptm")),
            "ranking_score": _safe_mean(summary.get("ranking_score")),
            "atom_plddts": mean_plddt,
            "pae": mean_pae,
            "chain_pair_pae_min": summary.get("chain_pair_pae_min"),
            "fraction_disordered": summary.get("fraction_disordered"),
            "has_clash": summary.get("has_clash"),
            "model_path": str(
                summary_file.parent / f"{prefix}_model.cif"),
        })

    df = pd.DataFrame(records)
    if df.empty:
        return df

    # Keep only the best sample per sequence (highest ranking_score)
    df = (df
          .sort_values("ranking_score", ascending=False)
          .drop_duplicates("id", keep="first")
          .reset_index(drop=True))
    return df


# ---------------------------------------------------------------------------
# Chai-1
# ---------------------------------------------------------------------------

def parse_chai_results(chai_dir: str) -> pd.DataFrame:
    """Parse Chai-1 score files.

    Expected directory layout::

        chai_dir/
          <seq_id>/
            output/
              scores.model_idx_0.npz
              scores.model_idx_1.npz
              ...

    For each sequence, takes the best (max) score across model indices.

    Returns a DataFrame with columns:
        id, aggregate_score, ptm, iptm
    """
    chai_path = Path(chai_dir)
    score_files = sorted(chai_path.rglob("scores.model_idx_*.npz"))
    if not score_files:
        return pd.DataFrame()

    seq_scores: dict[str, list[Path]] = defaultdict(list)
    for sf in score_files:
        # Walk up to find the seq-level directory (direct child of root)
        seq_id = sf.parent.name
        for parent in sf.parents:
            if parent.parent == chai_path:
                seq_id = parent.name
                break
        seq_scores[seq_id].append(sf)

    records: list[dict] = []
    for seq_id, files in seq_scores.items():
        agg_scores, ptms, iptms = [], [], []
        for f in files:
            res = np.load(f, allow_pickle=True)
            if "aggregate_score" in res:
                agg_scores.append(float(res["aggregate_score"][0]))
            if "ptm" in res:
                ptms.append(float(res["ptm"][0]))
            if "iptm" in res:
                iptms.append(float(res["iptm"][0]))
        records.append({
            "id": seq_id,
            "aggregate_score": float(np.max(agg_scores))
            if agg_scores else np.nan,
            "ptm": float(np.max(ptms)) if ptms else np.nan,
            "iptm": float(np.max(iptms)) if iptms else np.nan,
        })
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Boltz
# ---------------------------------------------------------------------------

def parse_boltz_results(boltz_dir: str) -> pd.DataFrame:
    """Parse Boltz prediction confidence outputs.

    Boltz writes results under ``boltz_results_<input_name>/`` with the
    following layout::

        boltz_dir/
          <seq_id>/
            boltz_results_<name>/
              predictions/
                <name>/
                  confidence_<name>_model_<idx>.json   # metrics
                  <name>_model_<idx>.cif               # structure

    The confidence JSON contains keys such as:
        confidence_score, ptm, iptm, ligand_iptm, protein_iptm,
        complex_plddt, complex_iplddt, pair_chains_iptm,
        per_chain_ptm, per_chain_plddt.

    Falls back to the simpler layout used in the existing test suite
    (``<seq_id>/predictions/result.json``) if no ``confidence_*.json``
    files are found.

    Returns a DataFrame with columns:
        id, confidence_score, ptm, iptm, ligand_iptm, protein_iptm,
        complex_plddt, complex_iplddt, model_path
    """
    boltz_path = Path(boltz_dir)
    records: list[dict] = []

    # Primary: confidence_*_model_*.json files (real Boltz output)
    conf_files = sorted(boltz_path.rglob("confidence_*_model_*.json"))

    if conf_files:
        for cf in conf_files:
            # Derive seq_id: walk up to find the seq-level directory
            # Layout: <seq_id>/boltz_results_<name>/predictions/<name>/confidence_...
            seq_id = _resolve_boltz_seq_id(cf, boltz_path)

            with open(cf) as f:
                data = json.load(f)

            # Corresponding structure file
            model_cif = cf.with_name(
                cf.name.replace("confidence_", "").replace(".json", ".cif"))

            records.append({
                "id": seq_id,
                "confidence_score": data.get("confidence_score", np.nan),
                "ptm": data.get("ptm", np.nan),
                "iptm": data.get("iptm", np.nan),
                "ligand_iptm": data.get("ligand_iptm", np.nan),
                "protein_iptm": data.get("protein_iptm", np.nan),
                "complex_plddt": data.get("complex_plddt", np.nan),
                "complex_iplddt": data.get("complex_iplddt", np.nan),
                "model_path": str(model_cif) if model_cif.exists() else "",
            })
    else:
        # Fallback: flat JSON files (e.g. <seq_id>/predictions/result.json)
        json_files = sorted(boltz_path.rglob("*.json"))
        for jf in json_files:
            if "manifest" in jf.name:
                continue
            seq_id = jf.parent.parent.name
            with open(jf) as f:
                data = json.load(f)
            records.append({
                "id": seq_id,
                "confidence_score": data.get("confidence_score", np.nan),
                "ptm": data.get("ptm", np.nan),
                "iptm": data.get("iptm", np.nan),
                "ligand_iptm": data.get("ligand_iptm", np.nan),
                "protein_iptm": data.get("protein_iptm", np.nan),
                "complex_plddt": data.get("complex_plddt", np.nan),
                "complex_iplddt": data.get("complex_iplddt", np.nan),
                "model_path": "",
            })

    df = pd.DataFrame(records)
    if df.empty:
        return df

    # Keep only the best model per sequence (highest confidence_score)
    df = (df
          .sort_values("confidence_score", ascending=False)
          .drop_duplicates("id", keep="first")
          .reset_index(drop=True))
    return df


def _resolve_boltz_seq_id(conf_file: Path, root: Path) -> str:
    """Walk up from a confidence JSON to find the sequence-level directory.

    We look for the first parent that is a direct child of *root* or that
    sits right above a ``boltz_results_*`` directory.
    """
    for parent in conf_file.parents:
        if parent == root:
            break
        if parent.parent == root:
            return parent.name
        if any(p.name.startswith("boltz_results_") for p in [parent]):
            return parent.parent.name
    # Fallback
    return conf_file.parent.parent.parent.parent.name


# ---------------------------------------------------------------------------
# LigandMPNN
# ---------------------------------------------------------------------------

def parse_ligandmpnn_results(ligandmpnn_dir: str) -> pd.DataFrame:
    """Parse LigandMPNN FASTA outputs.

    Recursively finds all ``.fa`` files under *ligandmpnn_dir*.
    The scaffold ID is derived from the file stem or, for nested layouts,
    from the ancestor directory that is a direct child of the root.

    Each .fa file contains FASTA records with headers like:
        >T=0.1, sample=1, score=0.5234, global_score=0.4321,
         seq_recovery=0.6543, id=1, overall_confidence=0.8765,
         ligand_confidence=0.7654

    Returns a DataFrame with columns:
        id, sequence, scaffold_id, sample_number,
        overall_confidence, ligand_confidence, seq_recovery
    """
    mpnn_path = Path(ligandmpnn_dir)
    records: list[dict] = []

    fa_pairs: list[tuple[Path, str]] = []
    for fa_file in sorted(mpnn_path.rglob("*.fa")):
        # Derive scaffold_id: use the top-level subdirectory name if nested,
        # otherwise use the file stem
        scaffold_id = fa_file.stem
        for parent in fa_file.parents:
            if parent.parent == mpnn_path:
                scaffold_id = parent.name
                break
        fa_pairs.append((fa_file, scaffold_id))

    for fa_file, scaffold_id in fa_pairs:
        header = None
        seq_lines: list[str] = []
        with open(fa_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(">"):
                    if header is not None and seq_lines:
                        _append_mpnn_record(
                            records, header, seq_lines, scaffold_id)
                    header = line
                    seq_lines = []
                else:
                    seq_lines.append(line)
            if header is not None and seq_lines:
                _append_mpnn_record(
                    records, header, seq_lines, scaffold_id)

    return pd.DataFrame(records)


def _append_mpnn_record(
    records: list, header: str, seq_lines: list, scaffold_id: str
) -> None:
    """Parse a single LigandMPNN FASTA record and append to records."""
    meta: dict[str, str] = {}
    for field in header[1:].split(", "):
        if "=" in field:
            k, v = field.split("=", 1)
            meta[k.strip()] = v.strip()
    if "id" in meta:
        records.append({
            "id": f"{scaffold_id}_seq{meta['id']}",
            "sequence": "".join(seq_lines),
            "scaffold_id": scaffold_id,
            "sample_number": int(meta["id"]),
            "overall_confidence": float(meta.get("overall_confidence", "nan")),
            "ligand_confidence": float(meta.get("ligand_confidence", "nan")),
            "seq_recovery": float(meta.get("seq_rec", "nan")),
        })


# ---------------------------------------------------------------------------
# CARBonAra
# ---------------------------------------------------------------------------

def parse_carbonara_results(carbonara_dir: str) -> pd.DataFrame:
    """Parse CARBonAra FASTA outputs.

    Recursively finds all ``.fasta`` files under *carbonara_dir*.
    Scaffold ID and sample number are derived from the filename
    (``<scaffold_id>_<N>.fasta``) or, for ``input_<N>.fasta`` files,
    from the parent directory name.

    Each FASTA contains a single record with an optional header like:
        >name, score=0.1234

    Returns a DataFrame with columns:
        id, sequence, scaffold_id, sample_number, score
    """
    carb_path = Path(carbonara_dir)
    records: list[dict] = []

    fa_pairs: list[tuple[Path, str, int]] = []
    for fa_file in sorted(carb_path.rglob("*.fasta")):
        # Try input_<N>.fasta — scaffold_id from parent directory
        input_match = re.match(r"^input_(\d+)\.fasta$", fa_file.name)
        if input_match:
            scaffold_id = fa_file.parent.name
            if scaffold_id == carb_path.name:
                scaffold_id = "unknown"
            sample_num = int(input_match.group(1))
        else:
            # Try <scaffold_id>_<N>.fasta
            match = re.match(r"^(.+)_(\d+)\.fasta$", fa_file.name)
            if match:
                scaffold_id = match.group(1)
                sample_num = int(match.group(2))
            else:
                scaffold_id = fa_file.stem
                sample_num = 0
        fa_pairs.append((fa_file, scaffold_id, sample_num))

    for fa_file, scaffold_id, sample_num in fa_pairs:
        header = None
        seq_lines: list[str] = []
        with open(fa_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(">"):
                    header = line
                else:
                    seq_lines.append(line)

        sequence = "".join(seq_lines)
        if not sequence:
            continue

        meta: dict[str, str] = {}
        if header:
            for field in header[1:].split(", "):
                if "=" in field:
                    k, v = field.split("=", 1)
                    meta[k.strip()] = v.strip()

        records.append({
            "id": f"{scaffold_id}_carb{sample_num}",
            "sequence": sequence,
            "scaffold_id": scaffold_id,
            "sample_number": sample_num,
            "score": float(meta.get("score", "nan")),
        })

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# RFDiffusion3 scaffolds
# ---------------------------------------------------------------------------

def parse_rfd3_results(rfd3_dir: str) -> pd.DataFrame:
    """Parse RFDiffusion3 scaffold outputs.

    Supports multiple directory layouts:

    1. Nested (original)::

        rfd3_dir/
          sample_<job>/
            <batch>/
              binding_site_0_denoised_model_<N>.cif
              binding_site_0_model_<N>.json

    2. Flat::

        rfd3_dir/
          <name>_model_<N>.cif[.gz]
          <name>_model_<N>.json

    Both ``.cif`` and ``.cif.gz`` structure files are recognised.
    When *denoised* CIF files exist they are preferred; otherwise all
    ``*_model_*.cif[.gz]`` files are used.

    Returns a DataFrame with columns:
        sample_id, structure_file, plus any keys from the metadata JSON.
    """
    rfd3_path = Path(rfd3_dir)
    records: list[dict] = []

    # Prefer denoised CIF files if any exist
    cif_files = sorted(rfd3_path.rglob("*_denoised_model_*.cif"))
    cif_files += sorted(rfd3_path.rglob("*_denoised_model_*.cif.gz"))

    if not cif_files:
        # Fallback: any *_model_*.cif[.gz] file
        cif_files = sorted(rfd3_path.rglob("*_model_*.cif"))
        cif_files += sorted(rfd3_path.rglob("*_model_*.cif.gz"))

    for cif_file in cif_files:
        sample_id = _rfd3_sample_id(cif_file)

        # Find matching metadata JSON:
        #   binding_site_0_denoised_model_0.cif -> binding_site_0_model_0.json
        #   demo_uncond_monomer_0_model_0.cif.gz -> demo_uncond_monomer_0_model_0.json
        base_name = cif_file.name
        if base_name.endswith(".gz"):
            base_name = base_name[:-3]
        json_name = base_name.replace("_denoised_", "_").replace(".cif", ".json")
        json_file = cif_file.parent / json_name

        meta: dict = {}
        if json_file.exists():
            with open(json_file) as f:
                meta = json.load(f)

        record: dict = {
            "sample_id": sample_id,
            "structure_file": str(cif_file),
        }
        for k, v in meta.items():
            record[k] = json.dumps(v) if isinstance(v, (dict, list)) else v
        records.append(record)

    return pd.DataFrame(records)


def _rfd3_sample_id(filepath: Path) -> str:
    """Build a unique sample ID from an RFD3 output path.

    Combines job directory (``sample_N``), batch subdirectory, and model
    number — e.g. ``sample_0_batch_0_model_0``.

    For flat layouts without ``sample_*`` directories, uses the filename
    stem (stripping ``.gz`` and ``_denoised`` portions) as the ID.
    """
    parts = filepath.parts
    # Handle .cif.gz — get the true stem
    filename = filepath.name
    if filename.endswith(".cif.gz"):
        filename = filename[:-7]  # strip .cif.gz
    elif filename.endswith(".cif"):
        filename = filename[:-4]  # strip .cif

    sample_dir = None
    sample_idx = -1
    for i, part in enumerate(parts):
        if part.startswith("sample_"):
            sample_dir = part
            sample_idx = i

    batch_dir = None
    if sample_idx >= 0 and sample_idx + 1 < len(parts):
        next_part = parts[sample_idx + 1]
        if next_part.isdigit():
            batch_dir = next_part

    # No sample_* directory found — flat layout, use full filename as ID
    if sample_dir is None:
        clean = filename.replace("_denoised", "")
        return clean

    model_match = re.search(r"model_(\d+)", filename)
    model_num = model_match.group(1) if model_match else None

    id_parts = [sample_dir]
    if batch_dir:
        id_parts.append(f"batch_{batch_dir}")
    if model_num is not None:
        id_parts.append(f"model_{model_num}")

    return "_".join(id_parts)


# ---------------------------------------------------------------------------
# Merge / ranking utilities
# ---------------------------------------------------------------------------

def merge_results(
    sequences_df: pd.DataFrame,
    af3_df: Optional[pd.DataFrame] = None,
    chai_df: Optional[pd.DataFrame] = None,
    boltz_df: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Merge sequence design records with structure-prediction metrics.

    Each validation DataFrame is left-joined onto *sequences_df* by ``id``.
    Metric columns are prefixed (``af3_``, ``chai_``, ``boltz_``) to avoid
    collisions.

    For AF3 results with multiple seeds/samples, only the best prediction
    per sequence (highest ``ranking_score``) is kept before merging.

    Args:
        sequences_df: Base DataFrame with at least an ``id`` column.
        af3_df: Output of :func:`parse_af3_results` (optional).
        chai_df: Output of :func:`parse_chai_results` (optional).
        boltz_df: Output of :func:`parse_boltz_results` (optional).

    Returns:
        Merged DataFrame.
    """
    result = sequences_df.copy()

    if af3_df is not None and len(af3_df) > 0:
        rename = {c: f"af3_{c}" for c in af3_df.columns if c != "id"}
        af3_renamed = af3_df.rename(columns=rename).drop(columns=["af3_source"], errors="ignore")
        result = result.merge(af3_renamed, on="id", how="left")

    if chai_df is not None and len(chai_df) > 0:
        rename = {c: f"chai_{c}" for c in chai_df.columns if c != "id"}
        chai_renamed = chai_df.rename(columns=rename)
        result = result.merge(chai_renamed, on="id", how="left")

    if boltz_df is not None and len(boltz_df) > 0:
        rename = {c: f"boltz_{c}" for c in boltz_df.columns if c != "id"}
        boltz_renamed = boltz_df.rename(columns=rename)
        result = result.merge(boltz_renamed, on="id", how="left")

    return result
