#!/usr/bin/env python3
"""Render comparison content for local review, with noindex enabled."""
from comparison_pages import ROOT, render_comparisons

if __name__ == '__main__':
    out = ROOT / 'output/comparison-preview'
    render_comparisons(out, preview=True)
    print('Local drafts: ' + str(out))
