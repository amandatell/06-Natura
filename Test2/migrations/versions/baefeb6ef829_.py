"""empty message

Revision ID: baefeb6ef829
Revises: 3daea1789082
Create Date: 2020-04-14 19:41:45.318446

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'baefeb6ef829'
down_revision = '3daea1789082'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_images')
    op.drop_table('places')
    op.drop_table('place_has_cat')
    op.drop_table('ratings')
    op.drop_table('is_in')
    op.drop_table('admin_images')
    op.drop_table('categories')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('categories_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='categories_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('admin_images',
    sa.Column('placeid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('pic', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('alt', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('imageid', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('datetime', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['placeid'], ['places.id'], name='admin_images_placeid_fkey'),
    sa.PrimaryKeyConstraint('imageid', name='admin_images_pkey')
    )
    op.create_table('is_in',
    sa.Column('place_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sub_place_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name='is_in_place_id_fkey'),
    sa.ForeignKeyConstraint(['sub_place_id'], ['places.id'], name='is_in_sub_place_id_fkey'),
    sa.PrimaryKeyConstraint('place_id', 'sub_place_id', name='is_in_pkey')
    )
    op.create_table('ratings',
    sa.Column('userid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('placeid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('datetime', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['placeid'], ['places.id'], name='ratings_placeid_fkey'),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], name='ratings_userid_fkey'),
    sa.PrimaryKeyConstraint('userid', 'placeid', name='ratings_pkey')
    )
    op.create_table('place_has_cat',
    sa.Column('cat_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('place_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['categories.id'], name='place_has_cat_cat_id_fkey'),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name='place_has_cat_place_id_fkey'),
    sa.PrimaryKeyConstraint('cat_id', 'place_id', name='place_has_cat_pkey')
    )
    op.create_table('places',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('places_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('source', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('latitude', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('longitude', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='places_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('user_images',
    sa.Column('userid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('placeid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('pic', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('alt', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('imageid', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('datetime', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['placeid'], ['places.id'], name='user_images_placeid_fkey'),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], name='user_images_userid_fkey'),
    sa.PrimaryKeyConstraint('userid', 'imageid', name='user_images_pkey')
    )
    # ### end Alembic commands ###