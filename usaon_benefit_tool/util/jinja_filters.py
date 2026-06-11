def humanize_enum(value):
    """Convert snake_case enum values to Title Case.
    
    Example: 'observing_system' -> 'Observing System'
    """
    if not value:
        return value
    return value.replace('_', ' ').title()
