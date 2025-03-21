import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import text_sensor, uartex
from esphome.const import CONF_ID, CONF_LAMBDA
from .. import uartex_ns, uint8_ptr_const, uint16_const, \
    state_schema, command_hex_schema, _uartex_declare_type
from ..const import CONF_STATE, CONF_COMMAND_UPDATE, CONF_UARTEX_ID

DEPENDENCIES = ['uartex']
UARTExTextSensor = uartex_ns.class_('UARTExTextSensor', text_sensor.TextSensor, cg.PollingComponent)

CONFIG_SCHEMA = cv.All(text_sensor.TEXT_SENSOR_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(UARTExTextSensor),
    cv.GenerateID(CONF_UARTEX_ID): _uartex_declare_type,
    cv.Optional(CONF_STATE): state_schema,
    cv.Optional(CONF_COMMAND_UPDATE): cv.templatable(command_hex_schema),
    cv.Required(CONF_LAMBDA): cv.returning_lambda,
}).extend(cv.polling_component_schema('60s')))

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await text_sensor.register_text_sensor(var, config)
    await uartex.register_uartex_device(var, config)
    
    if CONF_LAMBDA in config:
        template_ = await cg.templatable(config[CONF_LAMBDA], [(uint8_ptr_const, 'data'), (uint16_const, 'len')], cg.std_string)
        cg.add(var.set_state(CONF_LAMBDA, template_))
    
