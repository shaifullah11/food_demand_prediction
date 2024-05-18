# my_filters.py

from django import template
import re

register = template.Library()

@register.filter
def multiply_quantity(value, order):
    # Regular expression pattern to match the numeric value and unit
    pattern = r'(\d*\.?\d+)\s*(\D+)'
    
    # Extract the numeric value and unit using regular expression
    match = re.match(pattern, value)
    
    if match:
        quantity = int(float(match.group(1)) * order)
        unit = match.group(2)
        if unit == 'g' and quantity > 999:
            quantity = quantity/1000
            unit = 'kg'
            return f"{quantity} {(unit)}"
        if unit == 'ml' and quantity > 999:
            quantity = quantity/1000
            unit = 'L'
            return f"{quantity} {(unit)}"
        return f"{quantity} {(unit)}"  # Format the multiplied quantity with 2 decimal places
    else:
        return int(value)  # Return the original value if parsing fails
