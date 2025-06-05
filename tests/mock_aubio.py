# -*- coding: utf-8 -*-
"""
Mock module for aubio to simulate its functionality for testing purposes.
This allows tests to run without the actual aubio package installed.
"""

class Sink:
    def __init__(self, *args, **kwargs):
        pass

    def do(self, *args, **kwargs):
        pass

    def close(self):
        pass

class Source:
    def __init__(self, *args, **kwargs):
        pass

    def do(self, *args, **kwargs):
        return None

    def close(self):
        pass

class Tempo:
    def __init__(self, *args, **kwargs):
        pass

    def do(self, *args, **kwargs):
        return 0.0

    def get_last(self):
        return 0.0

class Pitch:
    def __init__(self, *args, **kwargs):
        pass

    def do(self, *args, **kwargs):
        return 0.0

    def get_last(self):
        return 0.0

class Onset:
    def __init__(self, *args, **kwargs):
        pass

    def do(self, *args, **kwargs):
        return 0.0

    def get_last(self):
        return 0.0

class Notes:
    def __init__(self, *args, **kwargs):
        pass

    def do(self, *args, **kwargs):
        return []

    def get_last(self):
        return []

class FVec:
    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, *args, **kwargs):
        return 0.0

    def __setitem__(self, *args, **kwargs):
        pass

class FMat:
    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, *args, **kwargs):
        return 0.0

    def __setitem__(self, *args, **kwargs):
        pass

# Mock functions
def hztomel(freq):
    return 0.0

def meltohz(mel):
    return 0.0

class filterbank:
    def __init__(self, *args, **kwargs):
        pass

    def set_triangle_bands(self, *args, **kwargs):
        pass

    def set_mel_coeffs(self, *args, **kwargs):
        pass

    def set_mel_coeffs_htk(self, *args, **kwargs):
        pass

    def set_mel_coeffs_slaney(self, *args, **kwargs):
        pass 