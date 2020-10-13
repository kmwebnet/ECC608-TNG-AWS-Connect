/* Auto-generated config file atca_config.h */
#ifndef ATCA_CONFIG_H
#define ATCA_CONFIG_H


/* Included device support */
#define ATCA_ATECC608A_SUPPORT
/** Define certificate templates to be supported. */
#define ATCA_TNGTLS_SUPPORT
/***************** Diagnostic & Test Configuration Section *****************/

/** Enable debug messages */
//#define ATCA_PRINTF

/******************** Features Configuration Section ***********************/

/** Define Software Crypto Library to Use - if none are defined use the
    cryptoauthlib version where applicable */
#define ATCA_MBEDTLS

/** Define to build atcab_ functions rather that defining them as macros */
#define ATCA_USE_ATCAB_FUNCTIONS

/* \brief How long to wait after an initial wake failure for the POST to
 *         complete.
 * If Power-on self test (POST) is enabled, the self test will run on waking
 * from sleep or during power-on, which delays the wake reply.
 */
#ifndef ATCA_POST_DELAY_MSEC
#define ATCA_POST_DELAY_MSEC 25
#endif

#define hal_delay_ms atca_delay_ms_internal

#endif // ATCA_CONFIG_H
