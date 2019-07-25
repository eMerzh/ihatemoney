"""Change date types to datetime

Revision ID: af2603235642
Revises: a67119aa3ee5
Create Date: 2019-07-25 14:56:43.303403

"""

# revision identifiers, used by Alembic.
revision = 'af2603235642'
down_revision = 'a67119aa3ee5'

from alembic import op
import sqlalchemy as sa

bill_helper = sa.Table(
    'bill', sa.MetaData(),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payer_id', sa.Integer()),
    sa.Column('amount', sa.Float()),
    sa.Column('date', sa.DateTime()),
    sa.Column('creation_date', sa.DateTime()),
    sa.Column('what', sa.UnicodeText()),
    sa.PrimaryKeyConstraint('id')
)

def upgrade():
    bind = op.get_bind()
    if bind.engine.name == 'sqlite':
        op.execute(
            bill_helper.update()
            .values(
                date=sa.func.datetime( bill_helper.c.date),
                creation_date=sa.func.datetime(bill_helper.c.creation_date)
            )
        )
    else:
        op.alter_column('bill', 'date', existing_type=sa.Date(), type_=sa.DateTime())
        op.alter_column('bill', 'creation_date', existing_type=sa.Date(), type_=sa.DateTime())


def downgrade():
    bind = op.get_bind()
    if bind.engine.name == 'sqlite':
        op.execute(
            bill_helper.update()
            .values(
                date=sa.func.strftime('%Y-%m-%d', bill_helper.c.date),
                creation_date=sa.func.strftime('%Y-%m-%d', bill_helper.c.creation_date)
            )
        )
    else:
        op.alter_column('bill', 'date', existing_type=sa.DateTime(), type_=sa.Date())
        op.alter_column('bill', 'creation_date', existing_type=sa.DateTime(), type_=sa.Date())
