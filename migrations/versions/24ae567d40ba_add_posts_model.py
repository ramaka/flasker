"""Add Posts Model

Revision ID: 24ae567d40ba
Revises: ad8f5c793071
Create Date: 2022-06-12 18:52:17.800409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24ae567d40ba'
down_revision = 'ad8f5c793071'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('slug', sa.String(length=255), nullable=True))
    op.add_column('posts', sa.Column('author', sa.String(length=255), nullable=True))
    op.add_column('posts', sa.Column('date_posted', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'date_posted')
    op.drop_column('posts', 'author')
    op.drop_column('posts', 'slug')
    # ### end Alembic commands ###
