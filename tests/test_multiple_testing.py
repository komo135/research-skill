from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "quant-research" / "scripts"))

import multiple_testing  # noqa: E402


def test_bonferroni_rejects_adjusted_pvalue_equal_to_alpha():
    pvalues = np.array([0.025, 0.5])

    rejected, adjusted = multiple_testing.bonferroni(pvalues, alpha=0.05)

    np.testing.assert_allclose(adjusted, np.array([0.05, 1.0]))
    np.testing.assert_array_equal(rejected, np.array([True, False]))


def test_benjamini_hochberg_rejects_adjusted_pvalue_equal_to_alpha():
    pvalues = np.array([0.025, 0.5])

    rejected, adjusted = multiple_testing.benjamini_hochberg(pvalues, alpha=0.05)

    np.testing.assert_allclose(adjusted, np.array([0.05, 0.5]))
    np.testing.assert_array_equal(rejected, np.array([True, False]))


def test_benjamini_hochberg_adjusted_pvalues_are_monotone_step_up_values():
    pvalues = np.array([0.03, 0.02, 0.8])

    rejected, adjusted = multiple_testing.benjamini_hochberg(pvalues, alpha=0.05)

    np.testing.assert_allclose(adjusted, np.array([0.045, 0.045, 0.8]))
    np.testing.assert_array_equal(rejected, np.array([True, True, False]))


def test_holm_adjusted_pvalues_are_monotone_step_down_values():
    pvalues = np.array([0.01, 0.03, 0.04])

    rejected, adjusted = multiple_testing.holm(pvalues, alpha=0.05)

    np.testing.assert_allclose(adjusted, np.array([0.03, 0.06, 0.06]))
    np.testing.assert_array_equal(rejected, np.array([True, False, False]))


def test_holm_maps_adjusted_pvalues_back_to_original_order():
    pvalues = np.array([0.04, 0.01, 0.03])

    rejected, adjusted = multiple_testing.holm(pvalues, alpha=0.05)

    np.testing.assert_allclose(adjusted, np.array([0.06, 0.03, 0.06]))
    np.testing.assert_array_equal(rejected, np.array([False, True, False]))


def test_holm_rejects_adjusted_pvalue_equal_to_alpha():
    pvalues = np.array([0.01, 0.025, 0.2])

    rejected, adjusted = multiple_testing.holm(pvalues, alpha=0.05)

    np.testing.assert_allclose(adjusted, np.array([0.03, 0.05, 0.2]))
    np.testing.assert_array_equal(rejected, np.array([True, True, False]))
