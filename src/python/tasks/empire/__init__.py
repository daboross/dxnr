from meta.registry_exports import Exports
from tasks.empire import visualize_passing_movement

exports = Exports().merge(visualize_passing_movement.exports)
