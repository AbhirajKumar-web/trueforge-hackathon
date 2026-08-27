#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

from utils import calculate_average

def test_normal_list():
    result = calculate_average([1, 2, 3, 4, 5])
    assert result == 3.0, f"Expected 3.0, got {result}"
    print("✓ Normal list average test passed: [1, 2, 3, 4, 5] -> 3.0")

def test_floats():
    result = calculate_average([1.5, 2.5, 5.0])
    assert result == 3.0, f"Expected 3.0, got {result}"
    print("✓ Float list average test passed: [1.5, 2.5, 5.0] -> 3.0")

def test_single_element():
    result = calculate_average([42])
    assert result == 42.0, f"Expected 42.0, got {result}"
    print("✓ Single element average test passed: [42] -> 42.0")

if __name__ == "__main__":
    test_normal_list()
    test_floats()
    test_single_element()
    print("\n🎉 Normal list tests passed!")
