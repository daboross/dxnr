from meta.registry_exports import Exports
from trename_processes import basic_upgrade_level1, bootup, economy, spawning

exports = Exports().merge(bootup.exports).merge(economy.exports).merge(basic_upgrade_level1.exports).merge(
    spawning.exports)
