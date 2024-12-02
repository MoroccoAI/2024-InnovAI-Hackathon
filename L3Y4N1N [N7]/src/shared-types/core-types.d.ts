/**
 *this file contains types that are shared between the core app and plugins 
 (or other external modules). These types represent the API of your core app 
 that plugins need to interact with. This file might define:
 *Shared interfaces for plugin communication.
 *Types for objects, functions, or services that are exposed to the plugins.
 *Generic types that can be used in both the core app and plugin code.
*/

/** In other means adrari : types that define the structure of your core app's API,
 *  which the plugins will use to interact with the core app */

/** types should be general enough to be used both in the core application
 * (main process) and in plugins (which are separate modules or packages). */

export interface PluginManifest {
  name: string
  version: string
  description: string
  main: string
}

export interface Plugin extends PluginManifest {
  main: string
  activate: () => void
  deactivate: () => void
}
