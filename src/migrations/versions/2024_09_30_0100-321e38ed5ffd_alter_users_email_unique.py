"""alter users email unique

Revision ID: 321e38ed5ffd
Revises: 111a52ce1750
Create Date: 2024-09-30 01:00:22.671756

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "321e38ed5ffd"
down_revision: Union[str, None] = "111a52ce1750"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
