"""rename closed status to private, add descriptions.

Revision ID: 31d9cf7fb54d
Revises: 2a175b3a16e1
Create Date: 2026-08-24 16:56:47.768833

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '31d9cf7fb54d'
down_revision: str | None = '2a175b3a16e1'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # New status (rename of 'closed')
    op.execute(
        "INSERT INTO status (id, description) VALUES "
        "('private', 'Complete but not available for viewing publicly')",
    )
    # Repoint any assessments using the old status
    op.execute(
        "UPDATE assessment SET status_id = 'private' WHERE status_id = 'closed'",
    )
    # Remove the old status
    op.execute("DELETE FROM status WHERE id = 'closed'")

    # Update the archived description (was 'TODO')
    op.execute(
        "UPDATE status SET description = "
        "'data saved but not available for viewing. Admins can still review.' "
        "WHERE id = 'archived'",
    )


def downgrade() -> None:
    op.execute("INSERT INTO status (id, description) VALUES ('closed', 'TODO')")
    op.execute(
        "UPDATE assessment SET status_id = 'closed' WHERE status_id = 'private'",
    )
    op.execute("DELETE FROM status WHERE id = 'private'")
    op.execute("UPDATE status SET description = 'TODO' WHERE id = 'archived'")
