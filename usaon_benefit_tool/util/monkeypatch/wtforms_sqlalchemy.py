from sqlalchemy import inspect as sainspect
from wtforms_sqlalchemy.orm import ModelConverter


def model_fields(  # noqa: C901, PLR0913
    model,
    db_session=None,
    only=None,
    exclude=None,
    field_args=None,
    converter=None,
    exclude_pk=False,  # noqa: FBT002
    exclude_fk=False,  # noqa: FBT002
):
    """Generate a dictionary of fields for a given SQLAlchemy model.

    See `model_form` docstring for description of parameters.

    FROM:
        https://github.com/wtforms/wtforms-sqlalchemy/blob/09b3d4745ec98d6d8f769f6794bc217c63d81946/wtforms_sqlalchemy/orm.py

    PATCHES:
        * Skip props that are polymorphic discriminators.
    """
    mapper = sainspect(model)
    converter = converter or ModelConverter()
    field_args = field_args or {}
    properties = []

    for prop in mapper.attrs.values():
        if getattr(prop, "_is_polymorphic_discriminator", False):
            continue
        if getattr(prop, "columns", None):
            if exclude_fk and prop.columns[0].foreign_keys:
                continue
            elif exclude_pk and prop.columns[0].primary_key:
                continue

        properties.append((prop.key, prop))

    # ((p.key, p) for p in mapper.iterate_properties)
    if only:
        properties = (x for x in properties if x[0] in only)
    elif exclude:
        properties = (x for x in properties if x[0] not in exclude)

    field_dict = {}
    for name, prop in properties:
        field = converter.convert(model, mapper, prop, field_args.get(name), db_session)

        if field is not None:
            field_dict[name] = field

    return field_dict
