"""tutor-stident-m2m

Revision ID: cf966c512342
Revises: 0f24b0ca682b
Create Date: 2024-05-26 11:31:43.329360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf966c512342'
down_revision: Union[str, None] = '0f24b0ca682b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tutor_student',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('tutor_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tutor_id'], ['tutor.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'student_id', 'tutor_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tutor_student')
    # ### end Alembic commands ###