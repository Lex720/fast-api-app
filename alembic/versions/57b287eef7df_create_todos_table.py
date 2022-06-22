"""create todos table

Revision ID: 57b287eef7df
Revises: 3946a3ed53f7
Create Date: 2022-06-20 21:35:58.553665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "57b287eef7df"
down_revision = "3946a3ed53f7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'))
    )


def downgrade() -> None:
    op.drop_table("todos")
