import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor, binary_sensor, number, button
from esphome.const import CONF_ID,\
    CONF_BATTERY_LEVEL, CONF_NAME, CONF_BRIGHTNESS, UNIT_PERCENT, DEVICE_CLASS_BATTERY, STATE_CLASS_MEASUREMENT, ENTITY_CATEGORY_DIAGNOSTIC

DEPENDENCIES = ['i2c']
AUTO_LOAD = ["binary_sensor", "number", "button"]
CONF_BATTERY_STATE = 'battery_state'
CONF_BATTERY_CHARGING = 'battery_charging'
CONF_POWEROFF = 'poweroff'

axp192_ns = cg.esphome_ns.namespace('axp192')
AXP192Component = axp192_ns.class_('AXP192Component', cg.PollingComponent, i2c.I2CDevice)
Brightness = axp192_ns.class_("Brightness", number.Number)
Poweroff = axp192_ns.class_("Poweroff", button.Button)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(AXP192Component),
    cv.Optional(CONF_BATTERY_LEVEL): sensor.sensor_schema(
        unit_of_measurement=UNIT_PERCENT,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_BATTERY,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_BATTERY_STATE): binary_sensor.binary_sensor_schema(
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_BATTERY_CHARGING): binary_sensor.binary_sensor_schema(
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_BRIGHTNESS): number.number_schema(Brightness),
    cv.Optional(CONF_POWEROFF): button.button_schema(Poweroff),
}).extend(cv.polling_component_schema("60s")).extend(i2c.i2c_device_schema(0x34))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if CONF_BATTERY_LEVEL in config:
        conf = config[CONF_BATTERY_LEVEL]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_batterylevel_sensor(sens))

    if CONF_BATTERY_STATE in config:
        conf = config[CONF_BATTERY_STATE]
        sens = await binary_sensor.new_binary_sensor(conf)
        cg.add(var.set_battery_state(sens))

    if CONF_BATTERY_CHARGING in config:
        conf = config[CONF_BATTERY_CHARGING]
        sens = await binary_sensor.new_binary_sensor(conf)
        cg.add(var.set_battery_charging(sens))

    if CONF_BRIGHTNESS in config:
        conf = config[CONF_BRIGHTNESS]
        sens = await number.new_number(conf,
            min_value = 0,
            max_value = 100,
            step = 0x01)
        cg.add(var.set_brightness(sens))

    if CONF_POWEROFF in config:
        conf = config[CONF_POWEROFF]
        sens = await button.new_button(conf)
        cg.add(var.set_poweroff(sens))
