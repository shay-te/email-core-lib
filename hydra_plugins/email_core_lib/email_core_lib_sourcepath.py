from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.core.config_search_path import ConfigSearchPath


class EmailCoreLibSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        assert isinstance(search_path, ConfigSearchPath)
        search_path.append("email_core_lib", "pkg://email_core_lib.email_core_lib.config")
