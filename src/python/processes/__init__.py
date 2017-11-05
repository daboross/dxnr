from meta.registry_exports import Exports
from processes import basic_upgrade_level1, bootup, economy, spawning, visualize_passing_movement

exports = (
    Exports()
        .merge(bootup.exports)
        .merge(economy.exports)
        .merge(basic_upgrade_level1.exports)
        .merge(spawning.exports)
        .merge(visualize_passing_movement.exports)
)
