"""Add user_id to Article model

Revision ID: 8e5c78bceb06
Revises: d9da94114026
Create Date: 2024-09-11 15:22:37.077613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e5c78bceb06'
down_revision = 'd9da94114026'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_article_user_id', 'user', ['user_id'], ['id'])

def downgrade():
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_constraint('fk_article_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')
        
    # ### end Alembic commands ###
