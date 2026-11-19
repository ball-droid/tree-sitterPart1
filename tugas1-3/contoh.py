import os
import sys
from pathlib import Path
from os import path


def sapa(nama):
    """Sapa satu orang."""
    print("halo", nama)
    return nama


def jumlah(a, b, c=0):
    total = a + b + c
    print(total)
    return total


class Alat:
    def jalan(self):
        # TODO: isi nanti
        print("jalan")

    def berhenti(self, paksa):
        if paksa:
            print("berhenti paksa")
