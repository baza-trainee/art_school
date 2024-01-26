"""change docs title len

Revision ID: 784da0913707
Revises: 5acc78c5d97d
Create Date: 2024-01-19 17:19:33.792525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "784da0913707"
down_revision: Union[str, None] = "5acc78c5d97d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "documents",
        "doc_name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=120),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "documents",
        "doc_name",
        existing_type=sa.String(length=120),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )

    # ### end Alembic commands ###
