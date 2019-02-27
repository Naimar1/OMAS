"""seventh migration

Revision ID: b1b11be491b9
Revises: 84140848962e
Create Date: 2019-02-27 11:37:15.175431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1b11be491b9'
down_revision = '84140848962e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('posted', sa.DateTime(), nullable=True))
    op.add_column('pitches', sa.Column('posted', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pitches', 'posted')
    op.drop_column('comments', 'posted')
    # ### end Alembic commands ###