# database/__init__.py

from .core import (
    db_client,
    get_mongo_stats,
    get_indexed_file_count,
    log_search_term,
    get_top_searched_terms,
    clear_search_logs
)

from .users import (
    add_user,
    is_user_exist,
    get_user_data,
    get_all_users
)

from .groups import (
    add_group,
    is_group_exist,
    get_group_data,
    get_all_groups
)

from .auth import (
    is_auth,
    add_auth,
    remove_auth,
    list_auth_users
)

from .premium import (
    is_premium,
    get_plan,
    set_premium,
    remove_premium,
    get_all_premium_users
)

from .shortener import (
    add_token_user,
    is_token_verified,
    clear_token_verification
)

from .settings import (
    get_group_settings,
    update_group_settings,
    get_all_group_settings
)

from .imdb_template import (
    get_imdb_template,
    set_imdb_template
)
