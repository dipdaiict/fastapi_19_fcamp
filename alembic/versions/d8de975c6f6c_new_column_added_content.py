"""New Column Added Content

Revision ID: d8de975c6f6c
Revises: 2180d3d73947
Create Date: 2024-01-24 12:35:34.172554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8de975c6f6c'
down_revision: Union[str, None] = '2180d3d73947'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
