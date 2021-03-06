"""create migration

Revision ID: f21d7d3be5a3
Revises: None
Create Date: 2016-05-27 13:09:35.420012

"""

# revision identifiers, used by Alembic.
revision = 'f21d7d3be5a3'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('projectName', sa.String(length=64), nullable=True),
    sa.Column('folderName', sa.String(length=64), nullable=True),
    sa.Column('remark', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('folderName')
    )
    op.create_index(op.f('ix_project_projectName'), 'project', ['projectName'], unique=True)
    op.create_table('suite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('suiteName', sa.String(length=64), nullable=True),
    sa.Column('remark', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_suite_suiteName'), 'suite', ['suiteName'], unique=True)
    op.create_table('module',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('moduleName', sa.String(length=64), nullable=True),
    sa.Column('fileName', sa.String(length=64), nullable=True),
    sa.Column('className', sa.String(length=64), nullable=True),
    sa.Column('remark', sa.Text(), nullable=True),
    sa.Column('projectId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['projectId'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_module_moduleName'), 'module', ['moduleName'], unique=False)
    op.create_table('testReport',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reportFile', sa.String(length=64), nullable=True),
    sa.Column('passNum', sa.Integer(), nullable=True),
    sa.Column('failedNum', sa.Integer(), nullable=True),
    sa.Column('errorNum', sa.Integer(), nullable=True),
    sa.Column('remark', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('suiteId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['suiteId'], ['suite.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_testReport_timestamp'), 'testReport', ['timestamp'], unique=False)
    op.create_table('testCase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('caseName', sa.String(length=64), nullable=True),
    sa.Column('funcName', sa.String(length=64), nullable=True),
    sa.Column('params', sa.Text(), nullable=True),
    sa.Column('remark', sa.Text(), nullable=True),
    sa.Column('moduleId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['moduleId'], ['module.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_testCase_caseName'), 'testCase', ['caseName'], unique=False)
    op.create_table('data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dataName', sa.String(length=64), nullable=True),
    sa.Column('values', sa.Text(), nullable=True),
    sa.Column('tags', sa.Text(), nullable=True),
    sa.Column('remark', sa.Text(), nullable=True),
    sa.Column('testCaseId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['testCaseId'], ['testCase.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('suiteData',
    sa.Column('suiteId', sa.Integer(), nullable=True),
    sa.Column('dataId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dataId'], ['data.id'], ),
    sa.ForeignKeyConstraint(['suiteId'], ['suite.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('suiteData')
    op.drop_table('data')
    op.drop_index(op.f('ix_testCase_caseName'), table_name='testCase')
    op.drop_table('testCase')
    op.drop_index(op.f('ix_testReport_timestamp'), table_name='testReport')
    op.drop_table('testReport')
    op.drop_index(op.f('ix_module_moduleName'), table_name='module')
    op.drop_table('module')
    op.drop_index(op.f('ix_suite_suiteName'), table_name='suite')
    op.drop_table('suite')
    op.drop_index(op.f('ix_project_projectName'), table_name='project')
    op.drop_table('project')
    ### end Alembic commands ###
