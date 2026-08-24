export type Style = Record<string, string>

export interface Geometry {
  x: number
  y: number
  width: number
  height: number
}

export interface Node {
  id: string
  label: string
  labelLines: string[]
  kind: 'start' | 'hub' | 'topic'
  groupId: string | null
  geometry: Geometry
  style: Style
  checkpoint: boolean
}

export interface Resource {
  title: string
  url: string
  detail?: string
}

export interface Topic extends Node {
  kind: 'topic'
  groupId: string
  resources: Resource[]
}

export interface Edge {
  id: string
  source: string
  target: string
  style: Style
  points: number[][]
}

export interface Group {
  id: string
  order: number
  title: string
  fill: string
  stroke: string
  hub: Node
  topicIds: string[]
}

export interface Ring {
  id: string
  geometry: Geometry
  style: Style
}

export interface RoadmapData {
  schemaVersion: number
  canvas: { width: number; height: number; background: string }
  start: Node
  groups: Group[]
  topics: Topic[]
  rings: Ring[]
  visibleEdges: Edge[]
  prerequisiteEdges: Edge[]
}
