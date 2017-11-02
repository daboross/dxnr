from meta.registry_exports import Exports
from tasks import empire

exports = Exports().merge(empire.exports)
