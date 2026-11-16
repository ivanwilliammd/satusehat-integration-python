"""@generated oleh scripts/generate_r5_namespace.py — jangan disunting tangan.

Lapisan R5: turunan apa adanya dari kelas kanon (R4). Selama R5 tidak mengubah resource ini,
memakai R5 cukup dengan mengganti baris import. Bila R5 memang berbeda, hapus penanda @generated
dan tulis implementasinya di sini.
"""
from __future__ import annotations

from src.builder.goal import GoalBuilder as _R4GoalBuilder


class GoalBuilder(_R4GoalBuilder):
    """R5: belum ada perbedaan terverifikasi terhadap R4."""
