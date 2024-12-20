"""Initial migration

Revision ID: e8f4d812b8e7
Revises:
Create Date: 2024-12-13 17:11:03.359482

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e8f4d812b8e7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column(
            "is_active", sa.Boolean(), server_default="true", nullable=False
        ),
        sa.Column(
            "role",
            sa.Enum("employee", "employer", name="userroleenum"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(
        op.f("ix_users_username"), "users", ["username"], unique=True
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "pending", "inprogress", "completed", name="taskstatusenum"
            ),
            server_default="pending",
            nullable=False,
        ),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("assignee_id", sa.Integer(), nullable=True),
        sa.Column("creator_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tasks_id"), "tasks", ["id"], unique=False)
    op.create_index(op.f("ix_tasks_title"), "tasks", ["title"], unique=False)
    op.create_foreign_key(
        "fk_tasks_creator_id_users", "tasks", "users", ["creator_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_tasks_assignee_id_users", "tasks", "users", ["assignee_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tasks_title"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_id"), table_name="tasks")
    op.drop_constraint("fk_tasks_creator_id_users", "tasks", type_="foreignkey")
    op.drop_constraint(
        "fk_tasks_assignee_id_users", "tasks", type_="foreignkey"
    )
    op.drop_table("tasks")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
