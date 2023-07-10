import math

def float_to_ordinal(number):
    # Check if the number is NaN
    if math.isnan(number):
        return "Invalid input: NaN"

    # Convert the float number to an integer
    integer_part = int(number)

    # Get the ordinal suffix based on the last digit of the integer
    suffix = "th" if 11 <= integer_part % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(integer_part % 10, "th")

    # Format the float value as a string with the ordinal suffix
    return f"{integer_part}{suffix}"