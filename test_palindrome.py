#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

from utils import is_palindrome

def test_basic_palindrome():
    """Test basic palindrome"""
    assert is_palindrome("racecar") == True
    print("✓ Basic palindrome test passed")

def test_palindrome_with_spaces():
    """Test palindrome with spaces"""
    assert is_palindrome("a man a plan a canal panama") == True
    print("✓ Palindrome with spaces test passed")

def test_palindrome_mixed_case():
    """Test palindrome with mixed case"""
    assert is_palindrome("RaceCar") == True
    print("✓ Palindrome mixed case test passed")

def test_not_palindrome():
    """Test non-palindrome"""
    assert is_palindrome("hello") == False
    print("✓ Not palindrome test passed")

def test_empty_string():
    """Test empty string"""
    assert is_palindrome("") == True
    print("✓ Empty string test passed")

def test_single_character():
    """Test single character"""
    assert is_palindrome("a") == True
    print("✓ Single character test passed")

def test_palindrome_with_numbers():
    """Test palindrome with numbers"""
    assert is_palindrome("12321") == True
    assert is_palindrome("12345") == False
    print("✓ Palindrome with numbers test passed")

def test_palindrome_phrase():
    """Test palindrome phrase with spaces and case"""
    assert is_palindrome("Was it a car or a cat I saw") == True
    print("✓ Palindrome phrase test passed")

def test_all_tests():
    """Run all tests"""
    test_basic_palindrome()
    test_palindrome_with_spaces()
    test_palindrome_mixed_case()
    test_not_palindrome()
    test_empty_string()
    test_single_character()
    test_palindrome_with_numbers()
    test_palindrome_phrase()
    print("\n🎉 All palindrome tests passed!")

if __name__ == "__main__":
    test_all_tests()