"""Phone Column Adding

Revision ID: 090feb94367e
Revises: aefb02ad602f
Create Date: 2024-01-24 13:49:32.790039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '090feb94367e'
down_revision: Union[str, None] = 'aefb02ad602f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Adding the "phone_no" column
    op.add_column('user_data', sa.Column('phone_no', sa.String(), nullable=True))  # Adjust the datatype accordingly

def downgrade():
    # Removing the "phone_no" column
    op.drop_column('user_data', 'phone_no')
