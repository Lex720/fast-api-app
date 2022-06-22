"""create users table

Revision ID: 3946a3ed53f7
Revises: 
Create Date: 2022-06-20 21:30:44.289938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3946a3ed53f7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, default=True),
        sa.Column("phone_number", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("users")
