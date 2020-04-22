"""empty message

Revision ID: 4daf13eab645
Revises: a7e6f9edaedd
Create Date: 2020-04-17 17:59:45.071055

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4daf13eab645'
down_revision = 'a7e6f9edaedd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Path')
    op.drop_table('Simulation')
    op.drop_table('Response')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Response',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Response_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('Simulation_Start', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Simulation_End', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('Year', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('Status', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Response_pkey')
    )
    op.create_table('Simulation',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Simulation_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('Simulation_Start', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('Simulation_End', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('Year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Status', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Simulation_pkey')
    )
    op.create_table('Path',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Path_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('Path', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Path_pkey')
    )
    # ### end Alembic commands ###