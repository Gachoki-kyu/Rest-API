"""adding columns to table post

Revision ID: ae52424a3a45
Revises: feba459e0c29
Create Date: 2024-12-22 02:42:40.305428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae52424a3a45'
down_revision: Union[str, None] = 'feba459e0c29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text("now()")))
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default="True"))
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
