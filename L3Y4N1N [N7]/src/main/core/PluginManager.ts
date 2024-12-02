import { app } from 'electron'
import { join } from 'path'
import fs from 'fs/promises'
import { existsSync } from 'fs'
// import { Plugin } from '../types'
import { Plugin, PluginManifest } from '../../shared-types/core-types'
import { pathToFileURL } from 'url' // Import pathToFileURL from the url module

const pluginDirPath = join(app.getPath('userData'), 'plugins')

export class PluginManager {
  private registeredPlugins: Plugin[] = []
  private activePlugins: Plugin[] = []

  constructor() {
    this.ensurePluginDirectory()
  }

  /**
   * Ensure the plugins directory exists in the userData folder.
   */
  private async ensurePluginDirectory(): Promise<void> {
    try {
      if (!existsSync(pluginDirPath)) {
        await fs.mkdir(pluginDirPath, { recursive: true })
        console.log(`[PluginManager] Created plugins directory: ${pluginDirPath}`)
      }
    } catch (error) {
      console.error(`[PluginManager] Failed to ensure plugins directory: ${error}`)
    }
  }

  /**
   * Load all plugins from the plugins directory.
   */
  public async loadAll(): Promise<void> {
    try {
      const pluginFolders = await fs.readdir(pluginDirPath)

      await Promise.all(pluginFolders.map((folder) => this.loadPlugin(folder)))

      console.log(`[PluginManager] Loaded ${this.registeredPlugins.length} plugins.`)
      console.log(`[PluginManager] Activated ${this.activePlugins.length} plugins.`)
    } catch (error) {
      console.error(`[PluginManager] Failed to load plugins: ${error}`)
    }
  }

  /**
   * Load a single plugin by its folder name.
   */
  private async loadPlugin(pluginFolder: string): Promise<void> {
    const pluginPath = join(pluginDirPath, pluginFolder)
    const manifestPath = join(pluginPath, 'package.json')

    try {
      if (!existsSync(manifestPath)) {
        console.warn(`[PluginManager] Plugin manifest not found: ${manifestPath}`)
        return
      }

      const manifest = await this.validateManifest(manifestPath)
      const plugin: Plugin = {
        ...manifest,
        main: join(pluginPath, manifest.main),
        activate: () => {},
        deactivate: () => {}
      }

      this.registeredPlugins.push(plugin)
      await this.activatePlugin(plugin)
    } catch (error) {
      console.error(`[PluginManager] Failed to load plugin in "${pluginFolder}": ${error}`)
    }
  }

  /**
   * Validate and parse the plugin manifest file.
   */
  private async validateManifest(manifestPath: string): Promise<Plugin> {
    try {
      // Read the manifest file
      const rawManifest = await fs.readFile(manifestPath, 'utf-8')

      // Parse the manifest file into a PluginManifest object
      const manifest = JSON.parse(rawManifest) as PluginManifest

      // Define required fields for validation
      const requiredFields = ['name', 'version', 'description', 'main']
      for (const field of requiredFields) {
        if (!manifest[field]) {
          throw new Error(`[PluginManager] Manifest is missing required field: ${field}`)
        }
      }

      // Return a Plugin object, adding the necessary activate and deactivate methods
      const plugin: Plugin = {
        ...manifest,
        activate: () => {
          console.log(`Plugin ${manifest.name} activated`)
        },
        deactivate: () => {
          console.log(`Plugin ${manifest.name} deactivated`)
        }
      }

      return plugin // Return the validated Plugin object
    } catch (error) {
      throw new Error(`[PluginManager] Invalid manifest at "${manifestPath}": ${error}`)
    }
  }

  /**
   * Activate a plugin.
   */
  private async activatePlugin(plugin: Plugin): Promise<void> {
    try {
      if (!existsSync(plugin.main)) {
        console.error(`[PluginManager] Plugin entry file not found: ${plugin.main}`)
        return
      }

      // Convert the plugin's entry path to a file URL
      const pluginUrl = pathToFileURL(plugin.main).href

      // Dynamically import the plugin using the file URL
      const pluginModule = await import(pluginUrl)

      if (pluginModule.activate && typeof pluginModule.activate === 'function') {
        await pluginModule.activate()
        this.activePlugins.push(plugin)
        console.log(`[PluginManager] Activated plugin: ${plugin.name}`)
      } else {
        console.warn(`[PluginManager] No activate function found for plugin: ${plugin.name}`)
      }
    } catch (error) {
      console.error(`[PluginManager] Failed to activate plugin: ${plugin.name}: ${error}`)
    }
  }

  /**
   * Unload all plugins, calling their deactivate methods.
   */
  public async unloadAll(): Promise<void> {
    for (const plugin of this.activePlugins) {
      try {
        await plugin.deactivate()
        console.log(`[PluginManager] Deactivated plugin: ${plugin.name}`)
      } catch (error) {
        console.error(`[PluginManager] Failed to deactivate plugin: ${plugin.name}: ${error}`)
      }
    }
    this.activePlugins = []
  }
}
