""" news, posters,slider_main2

Revision ID: 6b2e7ad861d0
Revises: 8b2b64e46b91
Create Date: 2023-11-24 10:01:02.378421

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6b2e7ad861d0"
down_revision: Union[str, None] = "8b2b64e46b91"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "slider_main",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=300), nullable=True),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("photo", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.alter_column(
        "news",
        "created_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
    op.add_column("posters", sa.Column("created_at", sa.DateTime(), nullable=True))
    op.drop_column("posters", "date")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "posters", sa.Column("date", sa.DATE(), autoincrement=False, nullable=True)
    )
    op.drop_column("posters", "created_at")
    op.alter_column(
        "news",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=True,
    )
    op.drop_table("slider_main")
    # ### end Alembic commands ###
