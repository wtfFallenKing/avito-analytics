"""fix issues with sqlalchemy

Revision ID: be752746cd20
Revises: cc66b2eef339
Create Date: 2024-03-14 03:04:50.117134

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "be752746cd20"
down_revision: Union[str, None] = "cc66b2eef339"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "storage_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("baseline", sa.Integer(), nullable=False),
        sa.Column("discounts", postgresql.ARRAY(sa.INTEGER()), nullable=False),
        sa.Column("happened_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "matrix_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("matrix_id", sa.Integer(), nullable=False),
        sa.Column("happened_at", sa.DateTime(), nullable=False),
        sa.Column(
            "type",
            postgresql.ENUM("CREATE", "UPDATE", "DELETE", name="matrix_logs_type_enum"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["matrix_id"], ["matrices.id"], ondelete="NO ACTION"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("matrix_logs")
    op.drop_table("storage_logs")
    # ### end Alembic commands ###
