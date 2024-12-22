"""create table for users

Revision ID: df61e365b3e2
Revises: ae52424a3a45
Create Date: 2024-12-22 03:00:12.606676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df61e365b3e2'
down_revision: Union[str, None] = 'ae52424a3a45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()"))
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
