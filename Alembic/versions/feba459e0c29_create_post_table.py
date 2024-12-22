"""create_post_table

Revision ID: feba459e0c29
Revises: 
Create Date: 2024-12-22 02:01:05.571637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'feba459e0c29'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass