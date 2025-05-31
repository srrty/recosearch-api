# alembic/env.py

import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 1) alembic 디렉터리 기준으로 프로젝트 루트(한 단계 위)를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 2) Alembic 설정 로드
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3) SQLAlchemy Base 와 모델들을 임포트
from db import Base                   # db.py 에서 선언된 Base
import models.paper                    # Paper 모델
import models.user                     # User 모델
# 만약 favorites/comments 모델도 있다면 여기에 추가로 import
# import models.favorite
# import models.comment

# 4) 자동 생성 시 참조할 메타데이터
target_metadata = Base.metadata

# --------------------------------------------------------------------

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
