"""create address table

Revision ID: 05120d53713d
Revises: 57b287eef7df
Create Date: 2022-06-20 21:41:23.994423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "05120d53713d"
down_revision = "57b287eef7df"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "address",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("address1", sa.String(), nullable=False),
        sa.Column("address2", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("postalcode", sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'))
    )


def downgrade():
    op.drop_table("address")
