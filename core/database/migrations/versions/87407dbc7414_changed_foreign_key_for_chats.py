"""changed foreign key for chats

Revision ID: 87407dbc7414
Revises: 1ff9c5f5fc53
Create Date: 2023-03-03 19:17:17.311838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87407dbc7414'
down_revision = '1ff9c5f5fc53'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('chats_owner_id_fkey', 'chats', type_='foreignkey')
    op.create_foreign_key(None, 'chats', 'users', ['owner_id'], ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chats', type_='foreignkey')
    op.create_foreign_key('chats_owner_id_fkey', 'chats', 'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###
