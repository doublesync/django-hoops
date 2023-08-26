from django.urls import path
from . import views

urlpatterns = [
    
    # Discord URL patterns
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("login/discord/", views.login_discord, name="login_discord"),
    path("login/discord/redirect/", views.login_discord_redirect, name="login_discord_redirect"),
    path("logout/", views.logout, name="logout"),

    # Player URL patterns
    path("player/<int:id>/", views.player, name="player"),
    path("player/upgrade/<int:id>/", views.upgrade_player, name="upgrade_player"),
    path("player/create/", views.create_player, name="create_player"),
    path("players/", views.free_agents, name="players"),
    path("logs/upgrades/<int:id>/", views.upgrade_logs, name="upgrade_logs"),
    path("logs/cash/<int:id>/", views.cash_logs, name="cash_logs"),
    path("players/builder/", views.mock_builder, name="mock_builder"),
    path("players/vitals/update/<int:id>/", views.update_player_vitals, name="update_player_vitals"),
    path("players/pending/update/", views.update_player_pending_upgrades, name="update_player_pending_upgrades"),
    path("player/physicals/edit/<int:id>/", views.edit_physicals, name="edit_physicals"),
    # path("players/free-agents/", views.free_agents, name="free_agents"),
    path("player/styles/<int:id>/", views.player_styles, name="player_styles"),
    path("player/cash/add/", views.add_player_cash, name="add_player_cash"),
    path("player/cash/take/", views.take_player_cash, name="take_player_cash"),
    path("player/daily/reward/collect/", views.daily_rewards, name="daily_rewards"),
    path("player/upgrade/scrape/<int:id>/", views.scrape_tendencies, name="scrape_tendencies"),
    path("player/integrate/", views.integrate_player, name="integrate_player"),

    # Team URL patterns
    path("team/<int:id>/", views.team, name="team"),
    path("teams/", views.teams, name="teams"),
    path("team/trade/", views.trade, name="trade"),
    path("team/trade/accept/<int:id>/", views.accept_trade, name="accept_trade"),
    path("team/trade/decline/<int:id>/", views.decline_trade, name="decline_trade"),
    path("trades/panel/", views.trade_panel, name="trade_panel"),
    path("team/trade/finalize/", views.check_finalize_trade, name="check_finalize_trade"),

    # Miscellaneous URL patterns
    path("upgrades/pending/", views.upgrades_pending, name="upgrades_pending"),
    path("frivolities/", views.frivolities, name="frivolities"),
    path("coupons/", views.coupons, name="coupons"),
    path("ads.txt", views.ad_view.as_view()),

    # Htmx URL patterns
    path("players/search/", views.check_player_search, name="check_player_search"),
    path("teams/search/", views.check_team_search, name="check_team_search"),
    path("coupons/redeem/", views.check_coupon_code, name="check_coupon_code"),
    path("keys/redeem/", views.check_license_key, name="check_license_key"),
    path("players/attributes/", views.check_starting_attributes, name="check_starting_attributes"),
    path("positions/count/", views.check_position_count, name="check_position_count"),
    path("upgrades/validate/", views.check_upgrade_validation, name="check_upgrade_validation"),
    path("players/leaders/", views.check_player_leaders, name="check_player_leaders"),
    path("metas/leaders/", views.check_meta_leaders, name="check_meta_leaders"),
    path("attributes/leaders/", views.check_attribute_leaders, name="check_attribute_leaders"),
    path("teams/roster/", views.check_team_roster, name="check_team_roster"),
    path("teams/trade/", views.check_trade_validation, name="check_trade_validation"),
    path("notifications/mark/read/", views.check_read_notification, name="check_read_notification"),
    path("player/daily/reward/", views.check_daily_reward, name="check_daily_reward"),
    path("player/weight/check/", views.check_weight_change, name="check_weight_change"),
    path("players/free-agents/search/", views.check_free_agent_search, name="check_free_agent_search"),
    path("contract/offer/", views.check_contract_offer, name="check_contract_offer"),
    path("contract/revoke/", views.check_contract_revoke, name="check_contract_revoke"),
    path("players/create/spent/", views.check_creation_spent, name="check_creation_spent"),
    path("players/integrate/", views.check_player_integration, name="check_player_integration"),

    # User URL patterns
    path("user/notifications/<int:id>/", views.notifications, name="notifications"),

    # API URL patterns
    path('players/cyberfaces/api/', views.cyberface_check, name='cyberface_check'),
    # path('players/auto-collect/', views.auto_collect, name='auto_collect'),
    # path('players/add-badge/', views.add_badge, name='add_badge'),

]