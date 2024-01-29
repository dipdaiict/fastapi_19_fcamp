"""Added all the remaining columns

Revision ID: bf0618a8a795
Revises: a3f4549386f5
Create Date: 2024-01-24 12:48:29.546195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf0618a8a795'
down_revision: Union[str, None] = 'a3f4549386f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adding the "published" column
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default=sa.text('TRUE'), nullable=False))

    # Adding the "created_at" column
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))

    # Adding the "user_id" column with foreign key constraint
    op.add_column('posts', sa.Column('user_id', sa.Integer(), sa.ForeignKey('user_data.id', ondelete='CASCADE'), nullable=False))

def downgrade() -> None:
    # Removing the "user_id" column
    op.drop_column('posts', 'user_id')

    # Removing the "created_at" column
    op.drop_column('posts', 'created_at')

    # Removing the "published" column
    op.drop_column('posts', 'published')