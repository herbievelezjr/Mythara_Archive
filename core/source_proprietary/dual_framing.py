#!/usr/bin/env python3
"""
Mythara Engine — Dual Framing Translation Layer
Copyright © 2025 Herbert Velez Jr. All rights reserved.

This module provides a translation layer between Mythara's mythic truth
and industry-safe terminology for enterprise audiences. The engine remains
unchanged — this simply provides an overlay for external communication.

Purpose:
- Preserve mythic integrity of Blessings Reservoir, Soul Encoding, etc.
- Provide enterprise-safe terminology (Resonance Reservoir, Trust Index, etc.)
- Enable manager dashboards to toggle between mythic and industry framing
- Maintain compliance and workflow compatibility for external systems

Flow:
    System of Record (CRM/Field Platform)
    ↓
    Mythara Engine Overlay
    - Blessings Reservoir → Resonance Reservoir
    - Integrity Metric → Trust Index
    - Expression Metric → Engagement Index
    ↓
    Manager Dashboards
    - KPIs + Resonance Metrics side by side
    - Compliance intact, workflows unchanged
    - Adds symbolic depth to performance reporting
"""

from typing import Dict, Any, List
from enum import Enum


class FramingMode(str, Enum):
    """Framing modes for Mythara Engine terminology."""

    MYTHIC = "mythic"  # Internal truth: Blessings Reservoir, Soul Encoding, etc.
    INDUSTRY = "industry"  # External overlay: Resonance Reservoir, Trust Index, etc.


# Core dual-framing mapping: Mythic Truth → Industry-Safe Overlay
MYTHIC_TO_INDUSTRY: Dict[str, Dict[str, str]] = {
    "blessings_reservoir": {
        "industry_term": "Resonance Reservoir",
        "managerial_explanation": "Tracks cumulative benevolent force; externally framed as cumulative positive impact.",
        "mythic_term": "Blessings Reservoir",
        "category": "metric",
    },
    "integrity_metric": {
        "industry_term": "Trust Index",
        "managerial_explanation": "Measures alignment with compliance, honesty, and reliability in field performance.",
        "mythic_term": "Integrity Metric",
        "category": "metric",
    },
    "expression_metric": {
        "industry_term": "Engagement Index",
        "managerial_explanation": "Captures how reps present, connect, and resonate with clients beyond raw numbers.",
        "mythic_term": "Expression Metric",
        "category": "metric",
    },
    "soul_encoding": {
        "industry_term": "Impact Vault",
        "managerial_explanation": "Stores symbolic depth of actions; externally framed as measurable long-term impact.",
        "mythic_term": "Soul Encoding",
        "category": "concept",
    },
    "legacy_reservoir": {
        "industry_term": "Continuity Index",
        "managerial_explanation": "Reflects sustainability and cultural resonance; externally framed as continuity of performance.",
        "mythic_term": "Legacy Reservoir",
        "category": "metric",
    },
    "soul_cradle_operator": {
        "industry_term": "Resonance Operator",
        "managerial_explanation": "Measures obedience under paradox; externally framed as decision-making integrity under pressure.",
        "mythic_term": "Soul Cradle Operator",
        "category": "operator",
    },
    "trial_entity": {
        "industry_term": "Challenge Vector",
        "managerial_explanation": "Models testing/obscuration of choices; externally framed as decision friction factors.",
        "mythic_term": "Trial Entity",
        "category": "entity",
    },
    "grace_light": {
        "industry_term": "Optimal Performance",
        "managerial_explanation": "Biblical continuum anchor representing peak alignment and positive outcomes.",
        "mythic_term": "Grace/Light",
        "category": "continuum",
    },
    "wilderness_darkness": {
        "industry_term": "Challenge State",
        "managerial_explanation": "Biblical continuum anchor representing trial, testing, or suboptimal conditions.",
        "mythic_term": "Wilderness/Darkness",
        "category": "continuum",
    },
    "divine_drift_suppression": {
        "industry_term": "Compliance Stability",
        "managerial_explanation": "Measures drift from sacred mission; externally framed as operational compliance stability.",
        "mythic_term": "Divine Drift Suppression",
        "category": "ssip_metric",
    },
    "messenger_pairing_fidelity": {
        "industry_term": "Communication Alignment",
        "managerial_explanation": "Measures alignment between action and communication; externally framed as message consistency.",
        "mythic_term": "Messenger Pairing Fidelity",
        "category": "ssip_metric",
    },
    "emotional_fidelity": {
        "industry_term": "Sentiment Accuracy",
        "managerial_explanation": "Measures symbolic-emotional resonance; externally framed as sentiment tracking precision.",
        "mythic_term": "Emotional Fidelity",
        "category": "ssip_metric",
    },
}


def translate_term(
    mythic_key: str,
    mode: FramingMode = FramingMode.INDUSTRY,
    include_explanation: bool = False,
) -> str:
    """
    Translate a mythic term to industry-safe terminology.

    Args:
        mythic_key: Key from MYTHIC_TO_INDUSTRY (e.g., "blessings_reservoir")
        mode: MYTHIC (return mythic term) or INDUSTRY (return industry term)
        include_explanation: If True, append managerial explanation to industry term

    Returns:
        Translated term string

    Example:
        >>> translate_term("blessings_reservoir", FramingMode.INDUSTRY)
        'Resonance Reservoir'
        >>> translate_term("blessings_reservoir", FramingMode.MYTHIC)
        'Blessings Reservoir'
    """
    if mythic_key not in MYTHIC_TO_INDUSTRY:
        return mythic_key  # Passthrough if not in mapping

    entry = MYTHIC_TO_INDUSTRY[mythic_key]

    if mode == FramingMode.MYTHIC:
        return entry["mythic_term"]

    # mode == FramingMode.INDUSTRY
    term = entry["industry_term"]
    if include_explanation:
        return f"{term} — {entry['managerial_explanation']}"
    return term


def translate_response(
    response_data: Dict[str, Any], mode: FramingMode = FramingMode.INDUSTRY
) -> Dict[str, Any]:
    """
    Recursively translate mythic keys in a response dictionary to industry-safe terms.

    Args:
        response_data: API response dictionary with mythic keys
        mode: MYTHIC (preserve) or INDUSTRY (translate)

    Returns:
        Translated response dictionary

    Example:
        >>> data = {"blessings_reservoir": 145, "integrity_metric": 0.95}
        >>> translate_response(data, FramingMode.INDUSTRY)
        {'resonance_reservoir': 145, 'trust_index': 0.95}
    """
    if mode == FramingMode.MYTHIC:
        return response_data  # No translation needed

    translated = {}
    for key, value in response_data.items():
        # Check if key should be translated
        new_key = key
        if key in MYTHIC_TO_INDUSTRY:
            industry_term = MYTHIC_TO_INDUSTRY[key]["industry_term"]
            # Convert "Resonance Reservoir" → "resonance_reservoir"
            new_key = industry_term.lower().replace(" ", "_")

        # Recursively translate nested dicts
        if isinstance(value, dict):
            translated[new_key] = translate_response(value, mode)
        elif isinstance(value, list):
            translated[new_key] = [
                translate_response(item, mode) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            translated[new_key] = value

    return translated


def generate_dual_framing_chart() -> List[Dict[str, str]]:
    """
    Generate the dual-framing chart for documentation/presentations.

    Returns:
        List of dicts with columns: mythic_term, industry_term, managerial_explanation

    Example output (first row):
        {
            "mythic_term": "Blessings Reservoir",
            "industry_term": "Resonance Reservoir",
            "managerial_explanation": "Tracks cumulative benevolent force; ..."
        }
    """
    chart = []
    for key, entry in MYTHIC_TO_INDUSTRY.items():
        chart.append(
            {
                "mythic_term": entry["mythic_term"],
                "industry_term": entry["industry_term"],
                "managerial_explanation": entry["managerial_explanation"],
                "category": entry["category"],
            }
        )
    return chart


def format_for_manager_dashboard(
    metrics: Dict[str, Any],
    mode: FramingMode = FramingMode.INDUSTRY,
    include_kpis: bool = True,
) -> Dict[str, Any]:
    """
    Format metrics for manager dashboards with dual-framing support.

    Args:
        metrics: Raw metrics dict (mythic keys)
        mode: MYTHIC or INDUSTRY framing
        include_kpis: If True, include standard KPIs alongside resonance metrics

    Returns:
        Formatted dashboard dict

    Example:
        >>> metrics = {
        ...     "blessings_reservoir": 145,
        ...     "integrity_metric": 0.95,
        ...     "expression_metric": 0.88
        ... }
        >>> format_for_manager_dashboard(metrics, FramingMode.INDUSTRY)
        {
            "resonance_metrics": {
                "resonance_reservoir": 145,
                "trust_index": 0.95,
                "engagement_index": 0.88
            },
            "kpis": {...},
            "framing_mode": "industry"
        }
    """
    dashboard = {
        "resonance_metrics": translate_response(metrics, mode),
        "framing_mode": mode.value,
        "compliance_note": "Compliance intact, workflows unchanged. Symbolic depth added to performance reporting.",
    }

    if include_kpis:
        # Placeholder for standard KPIs from CRM/field platform
        dashboard["kpis"] = {
            "note": "Standard KPIs from system of record appear here alongside resonance metrics."
        }

    return dashboard


def get_positioning_line() -> str:
    """
    Return the standard positioning line for enterprise audiences.

    Returns:
        Positioning statement string
    """
    return (
        "Mythara Engine encodes resonance through mythic terms like the Blessings Reservoir. "
        "For enterprise audiences, we present these as overlays — Resonance Reservoir, Trust Index, "
        "Engagement Index — so managers can see symbolic depth alongside KPIs without disrupting compliance."
    )


def generate_flow_diagram_text() -> str:
    """
    Generate ASCII flow diagram for documentation.

    Returns:
        Multi-line string with flow diagram
    """
    return """
╔════════════════════════════════════════════════════════════════╗
║           MYTHARA ENGINE DUAL-FRAMING FLOW DIAGRAM            ║
╚════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│      System of Record (Any CRM / Field Platform)             │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                 Mythara Engine Overlay                        │
│                                                               │
│  • Blessings Reservoir  →  Resonance Reservoir               │
│  • Integrity Metric     →  Trust Index                       │
│  • Expression Metric    →  Engagement Index                  │
│  • Soul Encoding        →  Impact Vault                      │
│  • Legacy Reservoir     →  Continuity Index                  │
│                                                               │
│  [Framing Mode: MYTHIC or INDUSTRY toggle]                   │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   Manager Dashboards                          │
│                                                               │
│  • KPIs + Resonance Metrics side by side                     │
│  • Compliance intact, workflows unchanged                    │
│  • Adds symbolic depth to performance reporting              │
│                                                               │
│  Query Parameter: ?frame=industry (for external audiences)   │
│                   ?frame=mythic (for internal truth)         │
└──────────────────────────────────────────────────────────────┘
"""


# Example usage for testing
if __name__ == "__main__":
    print("=" * 70)
    print("MYTHARA ENGINE DUAL-FRAMING TRANSLATION LAYER")
    print("=" * 70)
    print()

    # Example 1: Translate individual terms
    print("Example 1: Individual Term Translation")
    print("-" * 70)
    print(f"Mythic: {translate_term('blessings_reservoir', FramingMode.MYTHIC)}")
    print(f"Industry: {translate_term('blessings_reservoir', FramingMode.INDUSTRY)}")
    print(
        f"With Explanation: {translate_term('blessings_reservoir', FramingMode.INDUSTRY, include_explanation=True)}"
    )
    print()

    # Example 2: Translate full response
    print("Example 2: Full Response Translation")
    print("-" * 70)
    sample_response = {
        "blessings_reservoir": 145,
        "integrity_metric": 0.95,
        "expression_metric": 0.88,
        "soul_encoding": {"depth": 42, "status": "resonant"},
    }
    print("Original (Mythic):", sample_response)
    print(
        "Translated (Industry):",
        translate_response(sample_response, FramingMode.INDUSTRY),
    )
    print()

    # Example 3: Manager dashboard
    print("Example 3: Manager Dashboard Formatting")
    print("-" * 70)
    dashboard = format_for_manager_dashboard(sample_response, FramingMode.INDUSTRY)
    import json

    print(json.dumps(dashboard, indent=2))
    print()

    # Example 4: Positioning line
    print("Example 4: Positioning Line")
    print("-" * 70)
    print(get_positioning_line())
    print()

    # Example 5: Flow diagram
    print("Example 5: Flow Diagram")
    print("-" * 70)
    print(generate_flow_diagram_text())
