"""Add Competition and CompetitionAttempt models

Revision ID: 001_add_competition
Revises: 
Create Date: 2025-12-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_add_competition'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create competition table
    op.create_table(
        'competition',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(8), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('difficulty', sa.String(20), nullable=False),
        sa.Column('num_questions', sa.Integer(), default=10),
        sa.Column('time_limit', sa.Integer(), default=600),
        sa.Column('status', sa.String(20), default='waiting'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('started_at', sa.DateTime()),
        sa.Column('ended_at', sa.DateTime()),
        sa.Column('winner_id', sa.Integer()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.ForeignKeyConstraint(['creator_id'], ['user.id']),
        sa.ForeignKeyConstraint(['category_id'], ['category.id']),
        sa.ForeignKeyConstraint(['winner_id'], ['user.id']),
    )
    op.create_index('ix_competition_code', 'competition', ['code'])
    
    # Create competition_attempt table
    op.create_table(
        'competition_attempt',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('competition_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Float(), default=0.0),
        sa.Column('correct_answers', sa.Integer(), default=0),
        sa.Column('total_questions', sa.Integer()),
        sa.Column('time_taken', sa.Integer()),
        sa.Column('status', sa.String(20), default='in_progress'),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime()),
        sa.Column('answers', sa.JSON(), default={}),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['competition_id'], ['competition.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
    )


def downgrade():
    op.drop_table('competition_attempt')
    op.drop_table('competition')
