"""Add new SBA related fields.

Revision ID: b9357b81d2b0
Revises: ea1181510e10
Create Date: 2024-10-14 22:37:03.652801

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b9357b81d2b0'
down_revision: str | None = 'ea1181510e10'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'node_subtype_societal_benefit_area',
        sa.Column('name', sa.String(length=512), nullable=True),
    )
    op.add_column(
        'node_subtype_societal_benefit_area',
        sa.Column('short_name', sa.String(length=256), nullable=True),
    )
    op.add_column(
        'node_subtype_societal_benefit_area',
        sa.Column('description', sa.String(), nullable=True),
    )
    op.add_column(
        'node_subtype_societal_benefit_area',
        sa.Column('framework_name', sa.String(length=256), nullable=True),
    )
    op.add_column(
        'node_subtype_societal_benefit_area',
        sa.Column('framework_url', sa.String(length=512), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('node_subtype_societal_benefit_area', 'framework_url')
    op.drop_column('node_subtype_societal_benefit_area', 'framework_name')
    op.drop_column('node_subtype_societal_benefit_area', 'description')
    op.drop_column('node_subtype_societal_benefit_area', 'short_name')
    op.drop_column('node_subtype_societal_benefit_area', 'name')
    # ### end Alembic commands ###
