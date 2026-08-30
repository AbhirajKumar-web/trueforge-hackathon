def add_numbers(a, b):
    return a + b

def multiply_numbers(a, b):
    return a * b

def merge_intervals(intervals):
    """
    Takes a list of [start, end] integer pairs and returns merged intervals.
    
    Merges overlapping intervals and intervals that touch at boundaries.
    Result is sorted by start time with no overlaps.
    
    Args:
        intervals: List of [start, end] pairs
        
    Returns:
        List of merged [start, end] pairs, sorted by start
    """
    if not intervals:
        return []
    
    # Sort intervals by start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = []
    current_start, current_end = sorted_intervals[0]
    
    for start, end in sorted_intervals[1:]:
        # If intervals overlap or touch (start <= current_end), merge them
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            # No overlap, add the current interval and move to next
            merged.append([current_start, current_end])
            current_start, current_end = start, end
    
    # Don't forget the last interval
    merged.append([current_start, current_end])
    
    return merged

def is_palindrome(s):
    """
    Checks if a string is a palindrome, ignoring case and spaces.
    
    Args:
        s: Input string
        
    Returns:
        True if the string is a palindrome, False otherwise
    """
    # Remove spaces and convert to lowercase
    cleaned = ''.join(s.split()).lower()
    # Check if cleaned string reads the same forwards and backwards
    return cleaned == cleaned[::-1]