from ifs.app_init import initialize_app

app = initialize_app(
    config_object_path="ifs.default_settings", config_envvars="IFS_SETTINGS"
)
