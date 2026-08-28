#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

from utils import merge_intervals

def test_normal_overlap():
    """Test normal overlap: [1,4],[2,6] → [1,6]"""
    intervals = [[1, 4], [2, 6]]
    result = merge_intervals(intervals)
    expected = [[1, 6]]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Normal overlap test passed")

def test_fully_contained():
    """Test intervals fully contained: [1,10],[2,3] → [1,10]"""
    intervals = [[1, 10], [2, 3]]
    result = merge_intervals(intervals)
    expected = [[1, 10]]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Fully contained test passed")

def test_touching_boundaries():
    """Test touching boundaries: [1,3],[3,5] → [1,5]"""
    intervals = [[1, 3], [3, 5]]
    result = merge_intervals(intervals)
    expected = [[1, 5]]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Touching boundaries test passed")

def test_separate_intervals():
    """Test separate intervals: [1,2],[4,5] → [[1,2],[4,5]]"""
    intervals = [[1, 2], [4, 5]]
    result = merge_intervals(intervals)
    expected = [[1, 2], [4, 5]]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Separate intervals test passed")

def test_mixed_scenario():
    """Test mixed scenario with multiple merges"""
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    result = merge_intervals(intervals)
    expected = [[1, 6], [8, 10], [15, 18]]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Mixed scenario test passed")

def test_empty_list():
    """Test empty input"""
    intervals = []
    result = merge_intervals(intervals)
    expected = []
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Empty list test passed")

def test_single_interval():
    """Test single interval"""
    intervals = [[5, 10]]
    result = merge_intervals(intervals)
    expected = [[5, 10]]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Single interval test passed")

def test_unsorted_input():
    """Test that unsorted input gets handled correctly"""
    intervals = [[6, 7], [1, 3], [2, 4], [5, 6]]
    result = merge_intervals(intervals)
    expected = [[1, 4], [5, 7]]  # [1,3] and [2,4] merge to [1,4]; [5,6] and [6,7] merge to [5,7]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Unsorted input test passed")

def test_all_tests():
    """Run all tests"""
    test_normal_overlap()
    test_fully_contained()
    test_touching_boundaries()
    test_separate_intervals()
    test_mixed_scenario()
    test_empty_list()
    test_single_interval()
    test_unsorted_input()
    print("\n🎉 All tests passed!")

if __name__ == "__main__":
    test_all_tests()
