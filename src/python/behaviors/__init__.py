from behaviors import spawn_fill, upgrade
from meta.registry_exports import Exports

exports = Exports().merge(upgrade.exports).merge(spawn_fill.exports)
