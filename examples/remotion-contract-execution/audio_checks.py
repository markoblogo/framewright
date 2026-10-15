"""Fail before PCM conversion can clip an unsafe regenerated mix."""
import math


def validate_peak(peak):
    if not math.isfinite(peak) or not 0 <= peak < 1:
        raise ValueError(f'Unsafe PCM peak: {peak}; lower/rebuild the mix before writing')
