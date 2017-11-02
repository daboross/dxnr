from meta.registry_exports import Exports
from trename_processes import bootup, economy

exports = Exports().merge(bootup.exports).merge(economy.exports)
