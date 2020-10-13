#include <stddef.h>
#include "atca_cfgs.h"
#include "atca_iface.h"
#include "atca_device.h"

/** \defgroup config Configuration (cfg_)
 * \brief Logical device configurations describe the CryptoAuth device type and logical interface.
   @{ */

/* if the number of these configurations grows large, we can #ifdef them based on required device support */

/** \brief default configuration for an ECCx08A device */
ATCAIfaceCfg cfg_ateccx08a_i2c_default = {
    .iface_type             = ATCA_I2C_IFACE,
    .devtype                = ATECC608A,
    .atcai2c.slave_address  = 0xC0,
    .atcai2c.bus            = 0,
    .atcai2c.baud           = 100000,
    .wake_delay             = 1500,
    .rx_retries             = 20
};
