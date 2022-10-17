from sqlalchemy.schema import Column


def column_length(column: Column) -> int:
    """Dig into SQLAlchemy object metadata to get column length.

    E.g. for a `String(512)` column, return `512`.
    """
    length = column.property.columns[0].type.length
    return length
