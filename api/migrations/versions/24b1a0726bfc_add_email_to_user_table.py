"""Add email to user table

Revision ID: 24b1a0726bfc
Revises: dba93c3809e6
Create Date: 2023-03-27 11:50:04.044229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24b1a0726bfc'
down_revision = 'dba93c3809e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prompter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('prompter', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_prompter_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_prompter_username'), ['username'], unique=True)

    op.create_table('follower',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['prompter.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['prompter.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.create_table('work',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.Enum('default', 'fiction', 'nonfiction', 'poetry', 'drama', name='genre'), nullable=True),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('body', sa.String(length=8000), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('prompter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prompter_id'], ['prompter.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('work', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_work_timestamp'), ['timestamp'], unique=False)

    op.create_table('liker',
    sa.Column('liker_id', sa.Integer(), nullable=False),
    sa.Column('liked_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['liked_id'], ['work.id'], ),
    sa.ForeignKeyConstraint(['liker_id'], ['prompter.id'], ),
    sa.PrimaryKeyConstraint('liker_id', 'liked_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('liker')
    with op.batch_alter_table('work', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_work_timestamp'))

    op.drop_table('work')
    op.drop_table('follower')
    with op.batch_alter_table('prompter', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_prompter_username'))
        batch_op.drop_index(batch_op.f('ix_prompter_email'))

    op.drop_table('prompter')
    # ### end Alembic commands ###
