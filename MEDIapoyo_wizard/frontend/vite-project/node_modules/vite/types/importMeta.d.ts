// This file is an augmentation to the built-in ImportMeta interface
// Thus cannot contain any top-level imports
// <https://www.typescriptlang.org/docs/handbook/declaration-merging.html#module-augmentation>

interface ImportMetaEnv {
  [key: string]: any
  BASE_URL: string
  MODE: string
  DEV: boolean
  PROD: boolean
  SSR: boolean
}

interface ImportMeta {
  url: string

  readonly hot?: import('vite/types/hot').ViteHotContext

  readonly env: ImportMetaEnv

  glob: import('vite/types/importGlob').ImportGlobFunction
  /**
   * @deprecated Use `import.meta.glob('*', { eager: true })` instead
   */
  globEager: import('vite/types/importGlob').ImportGlobEagerFunction
}
