"""init everything

Revision ID: fd1c7f7a0caf
Revises: 
Create Date: 2020-08-18 12:52:58.065281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd1c7f7a0caf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manga_sites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_manga_sites_id'), 'manga_sites', ['id'], unique=False)
    op.create_index(op.f('ix_manga_sites_name'), 'manga_sites', ['name'], unique=False)
    op.create_index(op.f('ix_manga_sites_url'), 'manga_sites', ['url'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_description'), 'items', ['description'], unique=False)
    op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=False)
    op.create_index(op.f('ix_items_title'), 'items', ['title'], unique=False)
    op.create_table('mangas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.Column('finished', sa.Boolean(), nullable=True),
    sa.Column('thum_img', sa.String(), nullable=True),
    sa.Column('manga_site_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manga_site_id'], ['manga_sites.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mangas_id'), 'mangas', ['id'], unique=False)
    op.create_index(op.f('ix_mangas_last_update'), 'mangas', ['last_update'], unique=False)
    op.create_index(op.f('ix_mangas_name'), 'mangas', ['name'], unique=False)
    op.create_index(op.f('ix_mangas_thum_img'), 'mangas', ['thum_img'], unique=False)
    op.create_index(op.f('ix_mangas_url'), 'mangas', ['url'], unique=False)
    op.create_table('association',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('manga_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manga_id'], ['mangas.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('chapters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('page_url', sa.String(), nullable=True),
    sa.Column('type', sa.Enum('CHAPTER', 'VOLUME', 'MISC', name='mangaindextypeenum'), nullable=True),
    sa.Column('manga_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manga_id'], ['mangas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chapters_id'), 'chapters', ['id'], unique=False)
    op.create_index(op.f('ix_chapters_page_url'), 'chapters', ['page_url'], unique=False)
    op.create_index(op.f('ix_chapters_title'), 'chapters', ['title'], unique=False)
    op.create_index(op.f('ix_chapters_type'), 'chapters', ['type'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_chapters_type'), table_name='chapters')
    op.drop_index(op.f('ix_chapters_title'), table_name='chapters')
    op.drop_index(op.f('ix_chapters_page_url'), table_name='chapters')
    op.drop_index(op.f('ix_chapters_id'), table_name='chapters')
    op.drop_table('chapters')
    op.drop_table('association')
    op.drop_index(op.f('ix_mangas_url'), table_name='mangas')
    op.drop_index(op.f('ix_mangas_thum_img'), table_name='mangas')
    op.drop_index(op.f('ix_mangas_name'), table_name='mangas')
    op.drop_index(op.f('ix_mangas_last_update'), table_name='mangas')
    op.drop_index(op.f('ix_mangas_id'), table_name='mangas')
    op.drop_table('mangas')
    op.drop_index(op.f('ix_items_title'), table_name='items')
    op.drop_index(op.f('ix_items_id'), table_name='items')
    op.drop_index(op.f('ix_items_description'), table_name='items')
    op.drop_table('items')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_manga_sites_url'), table_name='manga_sites')
    op.drop_index(op.f('ix_manga_sites_name'), table_name='manga_sites')
    op.drop_index(op.f('ix_manga_sites_id'), table_name='manga_sites')
    op.drop_table('manga_sites')
    # ### end Alembic commands ###
