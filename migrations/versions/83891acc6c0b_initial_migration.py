"""Initial Migration

Revision ID: 83891acc6c0b
Revises: 
Create Date: 2022-10-26 17:48:41.440509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83891acc6c0b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('needs_rehash', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'needs_rehash')
    # ### end Alembic commands ###
