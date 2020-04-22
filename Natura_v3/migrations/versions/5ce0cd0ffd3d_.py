"""empty message

Revision ID: 5ce0cd0ffd3d
Revises: 3daea1789082
Create Date: 2020-04-15 02:28:54.879922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ce0cd0ffd3d'
down_revision = '3daea1789082'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ratings', sa.Column('placeis', sa.Integer(), nullable=False))
    op.add_column('ratings', sa.Column('ratings', sa.Integer(), nullable=True))
    op.drop_constraint('ratings_placeid_fkey', 'ratings', type_='foreignkey')
    op.create_foreign_key(None, 'ratings', 'places', ['placeis'], ['id'])
    op.drop_column('ratings', 'placeid')
    op.drop_column('ratings', 'rating')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ratings', sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('ratings', sa.Column('placeid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'ratings', type_='foreignkey')
    op.create_foreign_key('ratings_placeid_fkey', 'ratings', 'places', ['placeid'], ['id'])
    op.drop_column('ratings', 'ratings')
    op.drop_column('ratings', 'placeis')
    # ### end Alembic commands ###
