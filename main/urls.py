from django.urls import path
from . import views

urlpatterns = [
    # Home & login PATHS
    path(route="", view=views.home, name="home"),
    path(route="login/", view=views.login, name="login"),
    path(route="login/discord/", view=views.login_discord, name="login_discord"),
    path(
        route="login/discord/redirect/",
        view=views.login_discord_redirect,
        name="login_discord_redirect",
    ),
    path(route="logout/", view=views.logout, name="logout"),
    # Player PATHS
    path(route="player/<int:id>/", view=views.player, name="player"),
    path(
        route="player/upgrade/<int:id>/",
        view=views.upgrade_player,
        name="upgrade_player",
    ),
    path(route="player/create/", view=views.create_player, name="create_player"),
    path(route="players/", view=views.players, name="players"),
    path(route="logs/upgrades/<int:id>/", view=views.upgrade_logs, name="upgrade_logs"),
    path(route="logs/cash/<int:id>/", view=views.cash_logs, name="cash_logs"),
    path(route="players/builder/", view=views.mock_builder, name="mock_builder"),
    path(
        route="players/vitals/update/<int:id>/",
        view=views.update_player_vitals,
        name="update_player_vitals",
    ),
    path(
        route="players/pending/update/",
        view=views.update_player_pending_upgrades,
        name="update_player_pending_upgrades",
    ),
    path(
        route="player/physicals/edit/<int:id>/",
        view=views.edit_physicals,
        name="edit_physicals",
    ),
    path(route="players/free-agents/", view=views.free_agents, name="free_agents"),
    # Player Cash PATHS
    path(route="player/cash/add/", view=views.add_player_cash, name="add_player_cash"),
    path(
        route="player/cash/take/", view=views.take_player_cash, name="take_player_cash"
    ),
    path(
        route="player/daily/reward/collect/",
        view=views.daily_rewards,
        name="daily_rewards",
    ),
    # Team PATHS
    path(route="team/<int:id>/", view=views.team, name="team"),
    path(route="teams/", view=views.teams, name="teams"),
    path(route="team/trade/", view=views.trade, name="trade"),
    path(
        route="team/trade/accept/<int:id>/",
        view=views.accept_trade,
        name="accept_trade",
    ),
    path(
        route="team/trade/decline/<int:id>/",
        view=views.decline_trade,
        name="decline_trade",
    ),
    path(
        route="trades/panel/",
        view=views.trade_panel,
        name="trade_panel",
    ),
    path(
        route="team/trade/finalize/",
        view=views.check_finalize_trade,
        name="check_finalize_trade",
    ),
    # Misc PATHS
    path(
        route="upgrades/pending/", view=views.upgrades_pending, name="upgrades_pending"
    ),
    path(route="frivolities/", view=views.frivolities, name="frivolities"),
    path(route="coupons/", view=views.coupons, name="coupons"),
    # Check PATHS
    path(
        route="players/search/",
        view=views.check_player_search,
        name="check_player_search",
    ),
    path(route="teams/search/", view=views.check_team_search, name="check_team_search"),
    path(
        route="coupons/redeem/", view=views.check_coupon_code, name="check_coupon_code"
    ),
    path(
        route="players/attributes/",
        view=views.check_starting_attributes,
        name="check_starting_attributes",
    ),
    path(
        route="positions/count/",
        view=views.check_position_count,
        name="check_position_count",
    ),
    path(
        route="upgrades/validate/",
        view=views.check_upgrade_validation,
        name="check_upgrade_validation",
    ),
    path(
        route="players/leaders/",
        view=views.check_player_leaders,
        name="check_player_leaders",
    ),
    path(
        route="metas/leaders/",
        view=views.check_meta_leaders,
        name="check_meta_leaders",
    ),
    path(
        route="attributes/leaders/",
        view=views.check_attribute_leaders,
        name="check_attribute_leaders",
    ),
    path(
        route="teams/roster/",
        view=views.check_team_roster,
        name="check_team_roster",
    ),
    path(
        route="teams/trade/",
        view=views.check_trade_validation,
        name="check_trade_validation",
    ),
    path(
        route="notifications/mark/read/",
        view=views.check_read_notification,
        name="check_read_notification",
    ),
    path(
        route="player/daily/reward/",
        view=views.check_daily_reward,
        name="check_daily_reward",
    ),
    path(
        route="player/weight/check/",
        view=views.check_weight_change,
        name="check_weight_change",
    ),
    # User PATHS
    path(
        route="user/notifications/<int:id>/",
        view=views.notifications,
        name="notifications",
    ),
    # Ad PATHS
    path("ads.txt", views.ad_view.as_view()),
]
