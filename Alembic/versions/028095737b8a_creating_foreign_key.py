"""creating foreign key

Revision ID: 028095737b8a
Revises: df61e365b3e2
Create Date: 2024-12-22 03:03:28.461515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '028095737b8a'
down_revision: Union[str, None] = 'df61e365b3e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer, nullable=False))
    op.create_foreign_key("fk_user_id", "posts", "users", ["user_id"], ["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("fk_user_id", "posts", type_="foreignkey")
    op.drop_column("posts", "user_id")
    pass