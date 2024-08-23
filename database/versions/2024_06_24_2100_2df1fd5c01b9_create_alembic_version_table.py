"""create_alembic_version_table

Revision ID: 2df1fd5c01b9
Revises: 
Create Date: 2024-06-24 20:45:07.225786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2df1fd5c01b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('alembic_version',
                    sa.Column('version_num', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('version_num')
                    )


def downgrade() -> None:
    op.drop_table('alembic_version')

