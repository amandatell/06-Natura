"""empty message

Revision ID: aca1db88e325
Revises: b032392579af
Create Date: 2020-04-21 19:42:44.813105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aca1db88e325'
down_revision = 'b032392579af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ratings',
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('placeid', sa.Integer(), nullable=False),
    sa.Column('ratings', sa.Integer(), nullable=True),
    sa.Column('datetime', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['placeid'], ['places.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('userid', 'placeid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ratings')
    # ### end Alembic commands ###
