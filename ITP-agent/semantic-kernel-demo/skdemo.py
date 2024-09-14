from mdemo import LightModel

# A 'Plugin' AKA, an Agent tool in semantic kernel are the same thing
# https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-native-plugins?pivots=programming-language-python
# https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-native-plugins?pivots=programming-language-python
from typing import List, Optional, Annotated

class LightsPlugin:
    def __init__(self, lights: List[LightModel]):
        self._lights = lights

    @kernel_function
    async def get_lights(self) -> Annotated[List[LightModel], "An array of lights"]:
        """Gets a list of lights and their current state."""
        return self._lights

    @kernel_function
    async def change_state(
        self,
        change_state: LightModel
    ) -> Annotated[Optional[LightModel], "The updated state of the light; will return null if the light does not exist"]:
        """Changes the state of the light."""
        for light in self._lights:
            if light["id"] == change_state["id"]:
                light["is_on"] = change_state.get("is_on", light["is_on"])
                light["brightness"] = change_state.get("brightness", light["brightness"])
                light["hex"] = change_state.get("hex", light["hex"])
                return light
        return None
    

# Create the kernel
kernel = Kernel()

# Create dependencies for the plugin
lights = [
    {"id": 1, "name": "Table Lamp", "is_on": False, "brightness": 100, "hex": "FF0000"},
    {"id": 2, "name": "Porch light", "is_on": False, "brightness": 50, "hex": "00FF00"},
    {"id": 3, "name": "Chandelier", "is_on": True, "brightness": 75, "hex": "0000FF"},
]

# Create the plugin
lights_plugin = LightsPlugin(lights)

# Add the plugin to the kernel
kernel.add_plugin(lights_plugin)