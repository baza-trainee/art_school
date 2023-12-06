"""Slider main Changed available characters

Revision ID: 802f1d4a46ca
Revises: 6b2e7ad861d0
Create Date: 2023-11-30 16:36:19.952422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "802f1d4a46ca"
down_revision: Union[str, None] = "6b2e7ad861d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "slider_main",
        "title",
        existing_type=sa.VARCHAR(length=300),
        type_=sa.String(length=150),
        existing_nullable=True,
    )
    op.alter_column(
        "slider_main",
        "description",
        existing_type=sa.VARCHAR(length=2000),
        type_=sa.String(length=150),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "slider_main",
        "description",
        existing_type=sa.String(length=150),
        type_=sa.VARCHAR(length=2000),
        existing_nullable=True,
    )
    op.alter_column(
        "slider_main",
        "title",
        existing_type=sa.String(length=150),
        type_=sa.VARCHAR(length=300),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
