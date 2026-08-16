"""separate cpf, phone verification and revocable auth sessions

Revision ID: 7b9d2c4e6f81
Revises: fdae6f06aeb9
Create Date: 2026-08-14
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7b9d2c4e6f81"
down_revision: Union[str, None] = "fdae6f06aeb9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _drop_users_cpf_column() -> None:
    if op.get_bind().dialect.name == "sqlite":
        with op.batch_alter_table("users", recreate="always") as batch_op:
            batch_op.drop_column("cpf")
    else:
        op.drop_column("users", "cpf")


def _restore_users_cpf_column() -> None:
    if op.get_bind().dialect.name == "sqlite":
        with op.batch_alter_table("users", recreate="always") as batch_op:
            batch_op.add_column(sa.Column("cpf", sa.String(length=14), nullable=True))
        op.execute(sa.text("UPDATE users SET cpf = (SELECT number FROM cpfs WHERE cpfs.user_id = users.id_user)"))
        with op.batch_alter_table("users", recreate="always") as batch_op:
            batch_op.alter_column("cpf", existing_type=sa.String(length=14), nullable=False)
            batch_op.create_unique_constraint("uq_users_cpf", ["cpf"])
    else:
        op.add_column("users", sa.Column("cpf", sa.String(length=14), nullable=True))
        op.execute(sa.text("UPDATE users SET cpf = cpfs.number FROM cpfs WHERE cpfs.user_id = users.id_user"))
        op.alter_column("users", "cpf", existing_type=sa.String(length=14), nullable=False)
        op.create_unique_constraint("uq_users_cpf", "users", ["cpf"])


def upgrade() -> None:
    op.create_table(
        "cpfs",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("number", sa.String(length=14), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id_user"],
            name="fk_cpfs_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("number", name="uq_cpfs_number"),
    )
    op.execute(
        sa.text(
            "INSERT INTO cpfs (user_id, number) "
            "SELECT id_user, cpf FROM users"
        )
    )
    _drop_users_cpf_column()

    op.create_table(
        "phone_verification_codes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("code_hash", sa.String(length=255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("verified", sa.Boolean(), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "attempt_count >= 0",
            name="ck_phone_verification_codes_attempt_count_nonnegative",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_phone_verification_codes_phone_created_at",
        "phone_verification_codes",
        ["phone", "created_at"],
        unique=False,
    )

    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("refresh_token_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("replaced_by_session_id", sa.String(length=36), nullable=True),
        sa.Column("revocation_reason", sa.String(length=50), nullable=True),
        sa.CheckConstraint(
            "expires_at > created_at",
            name="ck_auth_sessions_expiry_after_creation",
        ),
        sa.ForeignKeyConstraint(
            ["replaced_by_session_id"],
            ["auth_sessions.id"],
            name="fk_auth_sessions_replaced_by_session_id",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id_user"],
            name="fk_auth_sessions_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "refresh_token_hash",
            name="uq_auth_sessions_refresh_token_hash",
        ),
    )
    op.create_index(
        "ix_auth_sessions_expires_at",
        "auth_sessions",
        ["expires_at"],
        unique=False,
    )
    op.create_index(
        "ix_auth_sessions_user_active",
        "auth_sessions",
        ["user_id", "revoked_at", "expires_at"],
        unique=False,
    )


def downgrade() -> None:
    _restore_users_cpf_column()

    op.drop_index("ix_auth_sessions_user_active", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_expires_at", table_name="auth_sessions")
    op.drop_table("auth_sessions")

    op.drop_index(
        "ix_phone_verification_codes_phone_created_at",
        table_name="phone_verification_codes",
    )
    op.drop_table("phone_verification_codes")
    op.drop_table("cpfs")
