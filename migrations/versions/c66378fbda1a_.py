"""empty message

Revision ID: c66378fbda1a
Revises: a34cf8274365
Create Date: 2021-04-18 19:57:37.485459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c66378fbda1a'
down_revision = 'a34cf8274365'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=4096), nullable=True),
    sa.Column('category', sa.String(length=4096), nullable=True),
    sa.Column('posted', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('comments', sa.Column('item_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comments', 'items', ['item_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'item_id')
    op.drop_table('items')
    # ### end Alembic commands ###
