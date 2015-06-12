/*------------------------------------------------------------------------
 *  Copyright 2007-2009 (c) Jeff Brown <spadix@users.sourceforge.net>
 *
 *  This file is part of the ZBar Bar Code Reader.
 *
 *  The ZBar Bar Code Reader is free software; you can redistribute it
 *  and/or modify it under the terms of the GNU Lesser Public License as
 *  published by the Free Software Foundation; either version 2.1 of
 *  the License, or (at your option) any later version.
 *
 *  The ZBar Bar Code Reader is distributed in the hope that it will be
 *  useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 *  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser Public License
 *  along with the ZBar Bar Code Reader; if not, write to the Free
 *  Software Foundation, Inc., 51 Franklin St, Fifth Floor,
 *  Boston, MA  02110-1301  USA
 *
 *  http://sourceforge.net/projects/zbar
 *------------------------------------------------------------------------*/
#ifndef _ZBAR_H_
#define _ZBAR_H_

/** @file
 * ZBar Barcode Reader C API definition
 */

/** @mainpage
 *
 * interface to the barcode reader is available at several levels.
 * most applications will want to use the high-level interfaces:
 *
 * @section high-level High-Level Interfaces
 *
 * these interfaces wrap all library functionality into an easy-to-use
 * package for a specific toolkit:
 * - the "GTK+ 2.x widget" may be used with GTK GUI applications.  a
 *   Python wrapper is included for PyGtk
 * - the @ref zbar::QZBar "Qt4 widget" may be used with Qt GUI
 *   applications
 * - the Processor interface (in @ref c-processor "C" or @ref
 *   zbar::Processor "C++") adds a scanning window to an application
 *   with no GUI.
 *
 * @section mid-level Intermediate Interfaces
 *
 * building blocks used to construct high-level interfaces:
 * - the ImageScanner (in @ref c-imagescanner "C" or @ref
 *   zbar::ImageScanner "C++") looks for barcodes in a library defined
 *   image object
 * - the Window abstraction (in @ref c-window "C" or @ref
 *   zbar::Window "C++") sinks library images, displaying them on the
 *   platform display
 * - the Video abstraction (in @ref c-video "C" or @ref zbar::Video
 *   "C++") sources library images from a video device
 *
 * @section low-level Low-Level Interfaces
 *
 * direct interaction with barcode scanning and decoding:
 * - the Scanner (in @ref c-scanner "C" or @ref zbar::Scanner "C++")
 *   looks for barcodes in a linear intensity sample stream
 * - the Decoder (in @ref c-decoder "C" or @ref zbar::Decoder "C++")
 *   extracts barcodes from a stream of bar and space widths
 */

#ifdef __cplusplus

/** C++ namespace for library interfaces */
namespace zbar {
    extern "C" {
#endif


/** @name Global library interfaces */
/*@{*/

/** "color" of element: bar or space. */
typedef enum zbar_color_e {
    ZBAR_SPACE = 0,    /**< light area or space between bars */
    ZBAR_BAR = 1,      /**< dark area or colored bar segment */
} zbar_color_t;

/** decoded symbol type. */
typedef enum zbar_symbol_type_e {
    ZBAR_NONE        =      0,  /**< no symbol decoded */
    ZBAR_PARTIAL     =      1,  /**< intermediate status */
    ZBAR_EAN8        =      8,  /**< EAN-8 */
    ZBAR_UPCE        =      9,  /**< UPC-E */
    ZBAR_ISBN10      =     10,  /**< ISBN-10 (from EAN-13). @since 0.4 */
    ZBAR_UPCA        =     12,  /**< UPC-A */
    ZBAR_EAN13       =     13,  /**< EAN-13 */
    ZBAR_ISBN13      =     14,  /**< ISBN-13 (from EAN-13). @since 0.4 */
    ZBAR_I25         =     25,  /**< Interleaved 2 of 5. @since 0.4 */
    ZBAR_CODE39      =     39,  /**< Code 39. @since 0.4 */
    ZBAR_PDF417      =     57,  /**< PDF417. @since 0.6 */
    ZBAR_QRCODE      =     64,  /**< QR Code. @since 0.10 */
    ZBAR_CODE128     =    128,  /**< Code 128 */
    ZBAR_SYMBOL      = 0x00ff,  /**< mask for base symbol type */
    ZBAR_ADDON2      = 0x0200,  /**< 2-digit add-on flag */
    ZBAR_ADDON5      = 0x0500,  /**< 5-digit add-on flag */
    ZBAR_ADDON       = 0x0700,  /**< add-on flag mask */
} zbar_symbol_type_t;

/** error codes. */
typedef enum zbar_error_e {
    ZBAR_OK = 0,                /**< no error */
    ZBAR_ERR_NOMEM,             /**< out of memory */
    ZBAR_ERR_INTERNAL,          /**< internal library error */
    ZBAR_ERR_UNSUPPORTED,       /**< unsupported request */
    ZBAR_ERR_INVALID,           /**< invalid request */
    ZBAR_ERR_SYSTEM,            /**< system error */
    ZBAR_ERR_LOCKING,           /**< locking error */
    ZBAR_ERR_BUSY,              /**< all resources busy */
    ZBAR_ERR_XDISPLAY,          /**< X11 display error */
    ZBAR_ERR_XPROTO,            /**< X11 protocol error */
    ZBAR_ERR_CLOSED,            /**< output window is closed */
    ZBAR_ERR_WINAPI,            /**< windows system error */
    ZBAR_ERR_NUM                /**< number of error codes */
} zbar_error_t;

/** decoder configuration options.
 * @since 0.4
 */
typedef enum zbar_config_e {
    ZBAR_CFG_ENABLE = 0,        /**< enable symbology/feature */
    ZBAR_CFG_ADD_CHECK,         /**< enable check digit when optional */
    ZBAR_CFG_EMIT_CHECK,        /**< return check digit when present */
    ZBAR_CFG_ASCII,             /**< enable full ASCII character set */
    ZBAR_CFG_NUM,               /**< number of boolean decoder configs */

    ZBAR_CFG_MIN_LEN = 0x20,    /**< minimum data length for valid decode */
    ZBAR_CFG_MAX_LEN,           /**< maximum data length for valid decode */

    ZBAR_CFG_POSITION = 0x80,   /**< enable scanner to collect position data */

    ZBAR_CFG_X_DENSITY = 0x100, /**< image scanner vertical scan density */
    ZBAR_CFG_Y_DENSITY,         /**< image scanner horizontal scan density */
} zbar_config_t;

/** retrieve runtime library version information.
 * @param major set to the running major version (unless NULL)
 * @param minor set to the running minor version (unless NULL)
 * @returns 0
 */
extern int zbar_version(unsigned *major,
                        unsigned *minor);

/** set global library debug level.
 * @param verbosity desired debug level.  higher values create more spew
 */
extern void zbar_set_verbosity(int verbosity);

/** increase global library debug level.
 * eg, for -vvvv
 */
extern void zbar_increase_verbosity(void);

/** retrieve string name for symbol encoding.
 * @param sym symbol type encoding
 * @returns the static string name for the specified symbol type,
 * or "UNKNOWN" if the encoding is not recognized
 */
extern const char *zbar_get_symbol_name(zbar_symbol_type_t sym);

/** retrieve string name for addon encoding.
 * @param sym symbol type encoding
 * @returns static string name for any addon, or the empty string
 * if no addons were decoded
 */
extern const char *zbar_get_addon_name(zbar_symbol_type_t sym);

/** parse a configuration string of the form "[symbology.]config[=value]".
 * the config must match one of the recognized names.
 * the symbology, if present, must match one of the recognized names.
 * if symbology is unspecified, it will be set to 0.
 * if value is unspecified it will be set to 1.
 * @returns 0 if the config is parsed successfully, 1 otherwise
 * @since 0.4
 */
extern int zbar_parse_config(const char *config_string,
                             zbar_symbol_type_t *symbology,
                             zbar_config_t *config,
                             int *value);

/** @internal type unsafe error API (don't use) */
extern int _zbar_error_spew(const void *object,
                            int verbosity);
extern const char *_zbar_error_string(const void *object,
                                      int verbosity);
extern zbar_error_t _zbar_get_error_code(const void *object);

/*@}*/

struct zbar_symbol_s;
typedef struct zbar_symbol_s zbar_symbol_t;

struct zbar_symbol_set_s;
typedef struct zbar_symbol_set_s zbar_symbol_set_t;


/*------------------------------------------------------------*/
/** @name Symbol interface
 * decoded barcode symbol result object.  stores type, data, and image
 * location of decoded symbol.  all memory is owned by the library
 */
/*@{*/

/** @typedef zbar_symbol_t
 * opaque decoded symbol object.
 */

/** symbol reference count manipulation.
 * increment the reference count when you store a new reference to the
 * symbol.  decrement when the reference is no longer used.  do not
 * refer to the symbol once the count is decremented and the
 * containing image has been recycled or destroyed.
 * @note the containing image holds a reference to the symbol, so you
 * only need to use this if you keep a symbol after the image has been
 * destroyed or reused.
 * @since 0.9
 */
extern void zbar_symbol_ref(const zbar_symbol_t *symbol,
                            int refs);

/** retrieve type of decoded symbol.
 * @returns the symbol type
 */
extern zbar_symbol_type_t zbar_symbol_get_type(const zbar_symbol_t *symbol);

/** retrieve data decoded from symbol.
 * @returns the data string
 */
extern const char *zbar_symbol_get_data(const zbar_symbol_t *symbol);

/** retrieve length of binary data.
 * @returns the length of the decoded data
 */
extern unsigned int zbar_symbol_get_data_length(const zbar_symbol_t *symbol);

/** retrieve a symbol confidence metric.
 * @returns an unscaled, relative quantity: larger values are better
 * than smaller values, where "large" and "small" are application
 * dependent.
 * @note expect the exact definition of this quantity to change as the
 * metric is refined.  currently, only the ordered relationship
 * between two values is defined and will remain stable in the future
 * @since 0.9
 */
extern int zbar_symbol_get_quality(const zbar_symbol_t *symbol);

/** retrieve current cache count.  when the cache is enabled for the
 * image_scanner this provides inter-frame reliability and redundancy
 * information for video streams.
 * @returns < 0 if symbol is still uncertain.
 * @returns 0 if symbol is newly verified.
 * @returns > 0 for duplicate symbols
 */
extern int zbar_symbol_get_count(const zbar_symbol_t *symbol);

/** retrieve the number of points in the location polygon.  the
 * location polygon defines the image area that the symbol was
 * extracted from.
 * @returns the number of points in the location polygon
 * @note this is currently not a polygon, but the scan locations
 * where the symbol was decoded
 */
extern unsigned zbar_symbol_get_loc_size(const zbar_symbol_t *symbol);

/** retrieve location polygon x-coordinates.
 * points are specified by 0-based index.
 * @returns the x-coordinate for a point in the location polygon.
 * @returns -1 if index is out of range
 */
extern int zbar_symbol_get_loc_x(const zbar_symbol_t *symbol,
                                 unsigned index);

/** retrieve location polygon y-coordinates.
 * points are specified by 0-based index.
 * @returns the y-coordinate for a point in the location polygon.
 * @returns -1 if index is out of range
 */
extern int zbar_symbol_get_loc_y(const zbar_symbol_t *symbol,
                                 unsigned index);

/** iterate the set to which this symbol belongs (there can be only one).
 * @returns the next symbol in the set, or
 * @returns NULL when no more results are available
 */
extern const zbar_symbol_t *zbar_symbol_next(const zbar_symbol_t *symbol);

/** retrieve components of a composite result.
 * @returns the symbol set containing the components
 * @returns NULL if the symbol is already a physical symbol
 * @since 0.10
 */
extern const zbar_symbol_set_t*
zbar_symbol_get_components(const zbar_symbol_t *symbol);

/** iterate components of a composite result.
 * @returns the first physical component symbol of a composite result
 * @returns NULL if the symbol is already a physical symbol
 * @since 0.10
 */
extern const zbar_symbol_t*
zbar_symbol_first_component(const zbar_symbol_t *symbol);

/** print XML symbol element representation to user result buffer.
 * @see http://zbar.sourceforge.net/2008/barcode.xsd for the schema.
 * @param symbol is the symbol to print
 * @param buffer is the inout result pointer, it will be reallocated
 * with a larger size if necessary.
 * @param buflen is inout length of the result buffer.
 * @returns the buffer pointer
 * @since 0.6
 */
extern char *zbar_symbol_xml(const zbar_symbol_t *symbol,
                             char **buffer,
                             unsigned *buflen);

/*@}*/

/*------------------------------------------------------------*/
/** @name Symbol Set interface
 * container for decoded result symbols associated with an image
 * or a composite symbol.
 * @since 0.10
 */
/*@{*/

/** @typedef zbar_symbol_set_t
 * opaque symbol iterator object.
 * @since 0.10
 */

/** reference count manipulation.
 * increment the reference count when you store a new reference.
 * decrement when the reference is no longer used.  do not refer to
 * the object any longer once references have been released.
 * @since 0.10
 */
extern void zbar_symbol_set_ref(const zbar_symbol_set_t *symbols,
                                int refs);

/** retrieve set size.
 * @returns the number of symbols in the set.
 * @since 0.10
 */
extern int zbar_symbol_set_get_size(const zbar_symbol_set_t *symbols);

/** set iterator.
 * @returns the first decoded symbol result in a set
 * @returns NULL if the set is empty
 * @since 0.10
 */
extern const zbar_symbol_t*
zbar_symbol_set_first_symbol(const zbar_symbol_set_t *symbols);

/*@}*/

/*@}*/

/*------------------------------------------------------------*/
/** @name Image Scanner interface
 * @anchor c-imagescanner
 * mid-level image scanner interface.
 * reads barcodes from 2-D images
 */
/*@{*/

struct zbar_image_scanner_s;
/** opaque image scanner object. */
typedef struct zbar_image_scanner_s zbar_image_scanner_t;

/** constructor. */
extern zbar_image_scanner_t *zbar_image_scanner_create(void);

/** destructor. */
extern void zbar_image_scanner_destroy(zbar_image_scanner_t *scanner);

const zbar_symbol_t *zbar_image_scanner_first_symbol(const zbar_image_scanner_t *iscn);

/** set config for indicated symbology (0 for all) to specified value.
 * @returns 0 for success, non-0 for failure (config does not apply to
 * specified symbology, or value out of range)
 * @see zbar_decoder_set_config()
 * @since 0.4
 */
extern int zbar_image_scanner_set_config(zbar_image_scanner_t *scanner,
                                         zbar_symbol_type_t symbology,
                                         zbar_config_t config,
                                         int value);

/** parse configuration string using zbar_parse_config()
 * and apply to image scanner using zbar_image_scanner_set_config().
 * @returns 0 for success, non-0 for failure
 * @see zbar_parse_config()
 * @see zbar_image_scanner_set_config()
 * @since 0.4
 */
static inline int
zbar_image_scanner_parse_config (zbar_image_scanner_t *scanner,
                                 const char *config_string)
{
    zbar_symbol_type_t sym;
    zbar_config_t cfg;
    int val;
    return(zbar_parse_config(config_string, &sym, &cfg, &val) ||
           zbar_image_scanner_set_config(scanner, sym, cfg, val));
}


/** remove any previously decoded results from the image scanner.
 * somewhat more efficient version of
 * zbar_image_set_symbols(image, NULL) which may retain memory for
 * subsequent decodes
 * @since 0.10
 */
extern void zbar_image_scanner_recycle(zbar_image_scanner_t *scanner);

/** retrieve decode results for last scanned image.
 * @returns the symbol set result container or NULL if no results are
 * available
 * @note the symbol set does not have its reference count adjusted;
 * ensure that the count is incremented if the results may be kept
 * after the next image is scanned
 * @since 0.10
 */
extern const zbar_symbol_set_t*
zbar_image_scanner_get_results(const zbar_image_scanner_t *scanner);

/** scan for symbols in provided image.  The image format must be
 * "Y800" or "GRAY".
 * @returns >0 if symbols were successfully decoded from the image,
 * 0 if no symbols were found or -1 if an error occurs
 * @see zbar_image_convert()
 * @since 0.9 - changed to only accept grayscale images
 */
extern int zbar_scan_image(zbar_image_scanner_t *scanner,
                           unsigned width, unsigned height, const unsigned char *data);

/*@}*/

/*------------------------------------------------------------*/
/** @name Decoder interface
 * @anchor c-decoder
 * low-level bar width stream decoder interface.
 * identifies symbols and extracts encoded data
 */
/*@{*/

struct zbar_decoder_s;
/** opaque decoder object. */
typedef struct zbar_decoder_s zbar_decoder_t;

/** decoder data handler callback function.
 * called by decoder when new data has just been decoded
 */
typedef void (zbar_decoder_handler_t)(zbar_decoder_t *decoder);

/** constructor. */
extern zbar_decoder_t *zbar_decoder_create(void);

/** destructor. */
extern void zbar_decoder_destroy(zbar_decoder_t *decoder);

/** set config for indicated symbology (0 for all) to specified value.
 * @returns 0 for success, non-0 for failure (config does not apply to
 * specified symbology, or value out of range)
 * @since 0.4
 */
extern int zbar_decoder_set_config(zbar_decoder_t *decoder,
                                   zbar_symbol_type_t symbology,
                                   zbar_config_t config,
                                   int value);

/** parse configuration string using zbar_parse_config()
 * and apply to decoder using zbar_decoder_set_config().
 * @returns 0 for success, non-0 for failure
 * @see zbar_parse_config()
 * @see zbar_decoder_set_config()
 * @since 0.4
 */
static inline int zbar_decoder_parse_config (zbar_decoder_t *decoder,
                                             const char *config_string)
{
    zbar_symbol_type_t sym;
    zbar_config_t cfg;
    int val;
    return(zbar_parse_config(config_string, &sym, &cfg, &val) ||
           zbar_decoder_set_config(decoder, sym, cfg, val));
}

/** clear all decoder state.
 * any partial symbols are flushed
 */
extern void zbar_decoder_reset(zbar_decoder_t *decoder);

/** mark start of a new scan pass.
 * clears any intra-symbol state and resets color to ::ZBAR_SPACE.
 * any partially decoded symbol state is retained
 */
extern void zbar_decoder_new_scan(zbar_decoder_t *decoder);

/** process next bar/space width from input stream.
 * the width is in arbitrary relative units.  first value of a scan
 * is ::ZBAR_SPACE width, alternating from there.
 * @returns appropriate symbol type if width completes
 * decode of a symbol (data is available for retrieval)
 * @returns ::ZBAR_PARTIAL as a hint if part of a symbol was decoded
 * @returns ::ZBAR_NONE (0) if no new symbol data is available
 */
extern zbar_symbol_type_t zbar_decode_width(zbar_decoder_t *decoder,
                                            unsigned width);

/** retrieve color of @em next element passed to
 * zbar_decode_width(). */
extern zbar_color_t zbar_decoder_get_color(const zbar_decoder_t *decoder);

/** retrieve last decoded data.
 * @returns the data string or NULL if no new data available.
 * the returned data buffer is owned by library, contents are only
 * valid between non-0 return from zbar_decode_width and next library
 * call
 */
extern const char *zbar_decoder_get_data(const zbar_decoder_t *decoder);

/** retrieve length of binary data.
 * @returns the length of the decoded data or 0 if no new data
 * available.
 */
extern unsigned int
zbar_decoder_get_data_length(const zbar_decoder_t *decoder);

/** retrieve last decoded symbol type.
 * @returns the type or ::ZBAR_NONE if no new data available
 */
extern zbar_symbol_type_t
zbar_decoder_get_type(const zbar_decoder_t *decoder);

/** setup data handler callback.
 * the registered function will be called by the decoder
 * just before zbar_decode_width() returns a non-zero value.
 * pass a NULL value to disable callbacks.
 * @returns the previously registered handler
 */
extern zbar_decoder_handler_t*
zbar_decoder_set_handler(zbar_decoder_t *decoder,
                         zbar_decoder_handler_t *handler);

/** associate user specified data value with the decoder. */
extern void zbar_decoder_set_userdata(zbar_decoder_t *decoder,
                                      void *userdata);

/** return user specified data value associated with the decoder. */
extern void *zbar_decoder_get_userdata(const zbar_decoder_t *decoder);

/*@}*/

/*------------------------------------------------------------*/
/** @name Scanner interface
 * @anchor c-scanner
 * low-level linear intensity sample stream scanner interface.
 * identifies "bar" edges and measures width between them.
 * optionally passes to bar width decoder
 */
/*@{*/

struct zbar_scanner_s;
/** opaque scanner object. */
typedef struct zbar_scanner_s zbar_scanner_t;

/** constructor.
 * if decoder is non-NULL it will be attached to scanner
 * and called automatically at each new edge
 * current color is initialized to ::ZBAR_SPACE
 * (so an initial BAR->SPACE transition may be discarded)
 */
extern zbar_scanner_t *zbar_scanner_create(zbar_decoder_t *decoder);

/** destructor. */
extern void zbar_scanner_destroy(zbar_scanner_t *scanner);

/** clear all scanner state.
 * also resets an associated decoder
 */
extern zbar_symbol_type_t zbar_scanner_reset(zbar_scanner_t *scanner);

/** mark start of a new scan pass. resets color to ::ZBAR_SPACE.
 * also updates an associated decoder.
 * @returns any decode results flushed from the pipeline
 * @note when not using callback handlers, the return value should
 * be checked the same as zbar_scan_y()
 * @note call zbar_scanner_flush() at least twice before calling this
 * method to ensure no decode results are lost
 */
extern zbar_symbol_type_t zbar_scanner_new_scan(zbar_scanner_t *scanner);

/** flush scanner processing pipeline.
 * forces current scanner position to be a scan boundary.
 * call multiple times (max 3) to completely flush decoder.
 * @returns any decode/scan results flushed from the pipeline
 * @note when not using callback handlers, the return value should
 * be checked the same as zbar_scan_y()
 * @since 0.9
 */
extern zbar_symbol_type_t zbar_scanner_flush(zbar_scanner_t *scanner);

/** process next sample intensity value.
 * intensity (y) is in arbitrary relative units.
 * @returns result of zbar_decode_width() if a decoder is attached,
 * otherwise @returns (::ZBAR_PARTIAL) when new edge is detected
 * or 0 (::ZBAR_NONE) if no new edge is detected
 */
extern zbar_symbol_type_t zbar_scan_y(zbar_scanner_t *scanner,
                                      int y);

/** process next sample from RGB (or BGR) triple. */
static inline zbar_symbol_type_t zbar_scan_rgb24 (zbar_scanner_t *scanner,
                                                    unsigned char *rgb)
{
    return(zbar_scan_y(scanner, rgb[0] + rgb[1] + rgb[2]));
}

/** retrieve last scanned width. */
extern unsigned zbar_scanner_get_width(const zbar_scanner_t *scanner);

/** retrieve sample position of last edge.
 * @since 0.10
 */
extern unsigned zbar_scanner_get_edge(const zbar_scanner_t *scn,
                                      unsigned offset,
                                      int prec);

/** retrieve last scanned color. */
extern zbar_color_t zbar_scanner_get_color(const zbar_scanner_t *scanner);

/*@}*/

#ifdef __cplusplus
    }
}

# include "zbar/Exception.h"
# include "zbar/Decoder.h"
# include "zbar/Scanner.h"
# include "zbar/Symbol.h"
# include "zbar/Image.h"
# include "zbar/ImageScanner.h"
# include "zbar/Video.h"
# include "zbar/Window.h"
# include "zbar/Processor.h"
#endif

#endif
