"""empty message

Revision ID: 78d083eb429c
Revises: 5ce0cd0ffd3d
Create Date: 2020-04-21 19:03:53.317497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78d083eb429c'
down_revision = '5ce0cd0ffd3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ratings', sa.Column('placeid', sa.Integer(), nullable=False))
    op.drop_constraint('ratings_placeis_fkey', 'ratings', type_='foreignkey')
    op.create_foreign_key(None, 'ratings', 'places', ['placeid'], ['id'])
    op.drop_column('ratings', 'placeis')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ratings', sa.Column('placeis', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'ratings', type_='foreignkey')
    op.create_foreign_key('ratings_placeis_fkey', 'ratings', 'places', ['placeis'], ['id'])
    op.drop_column('ratings', 'placeid')
    # ### end Alembic commands ###