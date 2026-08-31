import { useCallback, useEffect, useMemo, useRef, useState, type PointerEvent, type WheelEvent } from 'react'
import rawRoadmap from './generated/roadmap.json'
import type { Edge, Geometry, Group, Node, RoadmapData, Style, Topic } from './types'

const roadmap = rawRoadmap as unknown as RoadmapData

type Point = { x: number; y: number }
type Transform = { x: number; y: number; scale: number }

const MIN_SCALE = 0.12
const MAX_SCALE = 1.25
const REPOSITORY_URL = 'https://github.com/RX-00/robotics-control-roadmap'
const CORE_TRACK_DESCRIPTIONS: Record<string, string> = {
  F: 'The mathematical and computational tools used to formulate robot models, analyze algorithms, and solve the numerical problems that appear throughout robotics.',
  M: 'Methods for expressing a robot’s geometry, kinematics, dynamics, and actuation so its motion and forces can be predicted.',
  C: 'Principles and methods for using measurements to make a system follow desired behavior and remain stable despite disturbances and uncertainty.',
  E: 'Techniques for inferring a robot’s unobserved state—such as position, velocity, or map—from noisy sensors and a model.',
  P: 'Algorithms that find collision-free, feasible motions from a start configuration to a goal while respecting the robot and environment.',
  O: 'A framework for choosing control inputs that optimize an objective over time while satisfying dynamics and constraints.',
  R: 'Coordinated control of a robot’s many joints and tasks so the entire body moves, balances, and interacts as intended.',
  I: 'Control methods for physical interaction involving contact, friction, impacts, and force regulation between a robot and its environment.',
  L: 'Methods that use data to learn models, policies, or control components, often improving performance when hand-designed models are limited.',
  D: 'Methods for ensuring robots operate safely, including constraint enforcement, risk management, verification, and fault handling.',
  H: 'The engineering practices that turn control and planning methods into dependable physical systems, including sensing, software, calibration, and testing.',
}

function numberStyle(style: Style, key: string, fallback: number) {
  const value = Number(style[key])
  return Number.isFinite(value) ? value : fallback
}

function center(geometry: Geometry): Point {
  return { x: geometry.x + geometry.width / 2, y: geometry.y + geometry.height / 2 }
}

function clipToward(node: Node, toward: Point): Point {
  const nodeCenter = center(node.geometry)
  const dx = toward.x - nodeCenter.x
  const dy = toward.y - nodeCenter.y
  const scales = []
  if (Math.abs(dx) > 0.00001) scales.push(node.geometry.width / 2 / Math.abs(dx))
  if (Math.abs(dy) > 0.00001) scales.push(node.geometry.height / 2 / Math.abs(dy))
  const scale = Math.min(...scales)
  return Number.isFinite(scale)
    ? { x: nodeCenter.x + scale * dx, y: nodeCenter.y + scale * dy }
    : nodeCenter
}

function edgePath(edge: Edge, nodes: Map<string, Node>): string | null {
  const source = nodes.get(edge.source)
  const target = nodes.get(edge.target)
  if (!source || !target) return null
  const points = edge.points.map(([x, y]) => ({ x, y }))
  const firstTarget = points[0] ?? center(target.geometry)
  const lastSource = points.at(-1) ?? center(source.geometry)
  const start = source.kind === 'start' && target.kind === 'hub'
    ? center(source.geometry)
    : clipToward(source, firstTarget)
  const end = source.kind === 'start' && target.kind === 'hub'
    ? center(target.geometry)
    : clipToward(target, lastSource)
  return `M ${start.x.toFixed(1)} ${start.y.toFixed(1)} L ${[...points, end]
    .map((point) => `${point.x.toFixed(1)} ${point.y.toFixed(1)}`)
    .join(' L ')}`
}

function softWrap(label: string, maxCharacters: number) {
  const words = label.split(/\s+/)
  const lines: string[] = []
  let line = ''
  for (const word of words) {
    const next = line ? `${line} ${word}` : word
    if (line && next.length > maxCharacters) {
      lines.push(line)
      line = word
    } else {
      line = next
    }
  }
  if (line) lines.push(line)
  if (lines.length <= 3) return lines
  return [...lines.slice(0, 2), `${lines.slice(2).join(' ').slice(0, maxCharacters - 1).trim()}…`]
}

function distance(first: Point, second: Point) {
  return Math.hypot(first.x - second.x, first.y - second.y)
}

function midpoint(first: Point, second: Point): Point {
  return { x: (first.x + second.x) / 2, y: (first.y + second.y) / 2 }
}

function initialTransform(width: number, height: number): Transform {
  const scale = Math.min(0.65, Math.max(0.22, Math.min(width, height) / 1550))
  const roadmapCenter = center(roadmap.start.geometry)
  return { x: width / 2 - roadmapCenter.x * scale, y: height / 2 - roadmapCenter.y * scale, scale }
}

function hashNodeId() {
  const id = decodeURIComponent(window.location.hash.replace(/^#/, ''))
  return roadmap.topics.some((topic) => topic.id === id) || roadmap.groups.some((group) => group.hub.id === id) ? id : null
}

function MapNode({
  node,
  selected,
  dimmed,
  onSelect,
}: {
  node: Node
  selected: boolean
  dimmed: boolean
  onSelect: (id: string) => void
}) {
  const geometry = node.geometry
  const radius = numberStyle(node.style, 'arcSize', 18)
  const rawStrokeWidth = numberStyle(node.style, 'strokeWidth', 1.5)
  const strokeWidth = Math.ceil(rawStrokeWidth) + (rawStrokeWidth >= 3 ? 1 : 0)
  const fontSize = numberStyle(node.style, 'fontSize', 14) + 1
  const lines = softWrap(node.label, node.kind === 'hub' ? 28 : Math.max(18, Math.floor(geometry.width / 9)))
  const lineHeight = fontSize * 1.25
  const firstY = geometry.y + geometry.height / 2 - ((lines.length - 1) * lineHeight) / 2
  const isInteractive = node.kind === 'topic' || node.kind === 'hub'

  const activate = () => {
    if (isInteractive) onSelect(node.id)
  }

  return (
    <g
      className={`map-node ${isInteractive ? 'map-interactive' : ''} ${selected ? 'is-selected' : ''} ${dimmed ? 'is-dimmed' : ''}`}
      role={isInteractive ? 'button' : undefined}
      aria-label={isInteractive ? `Open ${node.label} details` : undefined}
      aria-pressed={isInteractive ? selected : undefined}
      tabIndex={isInteractive ? 0 : undefined}
      onPointerDown={isInteractive ? (event) => event.stopPropagation() : undefined}
      onClick={activate}
      onKeyDown={isInteractive ? (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault()
          activate()
        }
      } : undefined}
    >
      <title>{node.label}</title>
      <rect
        x={geometry.x}
        y={geometry.y}
        width={geometry.width}
        height={geometry.height}
        rx={radius}
        fill={node.style.fillColor ?? '#ffffff'}
        stroke={node.style.strokeColor ?? '#444444'}
        strokeWidth={strokeWidth}
      />
      <text
        x={geometry.x + geometry.width / 2}
        textAnchor="middle"
        fontSize={fontSize}
        fontWeight={node.kind === 'hub' || node.checkpoint || node.style.fontStyle === '1' ? 650 : 500}
        pointerEvents="none"
      >
        {lines.map((line, index) => <tspan key={line} x={geometry.x + geometry.width / 2} y={firstY + index * lineHeight}>{line}</tspan>)}
      </text>
    </g>
  )
}

function StartNode({ node, dimmed }: { node: Node; dimmed: boolean }) {
  const nodeCenter = center(node.geometry)
  const radius = Math.min(node.geometry.width, node.geometry.height) / 2
  const [title = node.label, subtitle = '', ...legend] = node.labelLines
  return (
    <g className={`map-start ${dimmed ? 'is-dimmed' : ''}`}>
      <circle cx={nodeCenter.x} cy={nodeCenter.y} r={radius} fill={node.style.fillColor ?? '#fff'} stroke={node.style.strokeColor ?? '#202124'} strokeWidth="5" />
      <text x={nodeCenter.x} y={nodeCenter.y - 40} textAnchor="middle" fontSize="38" fontWeight="750">{title}</text>
      {subtitle && <text x={nodeCenter.x} y={nodeCenter.y + 78} textAnchor="middle" fontSize="18" fill="#5f6368">{subtitle}</text>}
      {legend.slice(0, 2).map((line, index) => <text key={line} x={nodeCenter.x} y={nodeCenter.y + 160 + index * 21} textAnchor="middle" fontSize="14" fill="#80868b">{line}</text>)}
    </g>
  )
}

function TopicPanel({
  topic,
  prerequisites,
  nextTopics,
  onNavigate,
  onClose,
}: {
  topic: Topic
  prerequisites: Topic[]
  nextTopics: Topic[]
  onNavigate: (id: string) => void
  onClose: () => void
}) {
  return (
    <aside className="topic-panel" aria-label={`${topic.label} details`}>
      <div className="panel-handle" aria-hidden="true" />
      <div className="panel-heading">
        <div>
          <p className="topic-kicker"><span style={{ background: topic.style.strokeColor }} />{topic.groupId} · Topic {topic.id}</p>
          <h2>{topic.label}</h2>
        </div>
        <button className="close-button" onClick={onClose} aria-label="Close topic details">×</button>
      </div>

      <section>
        <h3>Learning resources</h3>
        {topic.resources.length ? (
          <ul className="resource-list">
            {topic.resources.map((resource) => (
              <li key={resource.url}>
                <a href={resource.url} target="_blank" rel="noreferrer">{resource.title}<span aria-hidden="true"> ↗</span></a>
                {resource.detail && <p>{resource.detail}</p>}
              </li>
            ))}
          </ul>
        ) : <p className="empty-state">Curated resources for this topic are planned for a future content pass.</p>}
      </section>

      <section className="relationship-section">
        <h3>Prerequisites</h3>
        {prerequisites.length ? <TopicLinks topics={prerequisites} onNavigate={onNavigate} /> : <p className="empty-state">No direct prerequisite topics are recorded.</p>}
      </section>
      <section className="relationship-section">
        <h3>Next topics</h3>
        {nextTopics.length ? <TopicLinks topics={nextTopics} onNavigate={onNavigate} /> : <p className="empty-state">No direct next topics are recorded.</p>}
      </section>
    </aside>
  )
}

function CoreTrackPanel({ group, onClose }: { group: Group; onClose: () => void }) {
  return (
    <aside className="topic-panel core-track-panel" aria-label={`${group.title} overview`}>
      <div className="panel-handle" aria-hidden="true" />
      <div className="panel-heading">
        <div>
          <p className="topic-kicker"><span style={{ background: group.stroke }} />Core track</p>
          <h2>{group.title}</h2>
        </div>
        <button className="close-button" onClick={onClose} aria-label="Close track overview">×</button>
      </div>
      <section className="core-description">
        <h3>Overview</h3>
        <p>{CORE_TRACK_DESCRIPTIONS[group.id]}</p>
      </section>
    </aside>
  )
}

function TopicLinks({ topics, onNavigate }: { topics: Topic[]; onNavigate: (id: string) => void }) {
  return <ul className="topic-links">
    {topics.map((topic) => <li key={topic.id}><button onClick={() => onNavigate(topic.id)}><span>{topic.id}</span>{topic.label}</button></li>)}
  </ul>
}

export default function App() {
  const svgRef = useRef<SVGSVGElement>(null)
  const transformRef = useRef<Transform>({ x: 0, y: 0, scale: 1 })
  const animationFrame = useRef<number | null>(null)
  const pointers = useRef(new Map<number, Point>())
  const gesture = useRef<{ origin: Transform; start: Point; worldAnchor?: Point; startDistance?: number }>({ origin: transformRef.current, start: { x: 0, y: 0 } })
  const hasInitialized = useRef(false)
  const initialDeepLinkScheduled = useRef(false)
  const [transform, setTransform] = useState<Transform>(transformRef.current)
  const [selectedId, setSelectedId] = useState<string | null>(hashNodeId)
  const [hintVisible, setHintVisible] = useState(() => window.localStorage.getItem('roadmap-onboarding-dismissed') !== '1')

  const nodes = useMemo(() => new Map<string, Node>([
    [roadmap.start.id, roadmap.start] as [string, Node],
    ...roadmap.groups.map((group) => [group.hub.id, group.hub] as [string, Node]),
    ...roadmap.topics.map((topic) => [topic.id, topic] as [string, Node]),
  ]), [])
  const topicsById = useMemo(() => new Map(roadmap.topics.map((topic) => [topic.id, topic])), [])
  const groupById = useMemo(() => new Map(roadmap.groups.map((group) => [group.id, group])), [])
  const groupsByHubId = useMemo(() => new Map(roadmap.groups.map((group) => [group.hub.id, group])), [])

  const updateTransform = useCallback((next: Transform) => {
    transformRef.current = next
    setTransform(next)
  }, [])

  const stopAnimation = useCallback(() => {
    if (animationFrame.current !== null) cancelAnimationFrame(animationFrame.current)
    animationFrame.current = null
  }, [])

  const animateTo = useCallback((next: Transform) => {
    stopAnimation()
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      updateTransform(next)
      return
    }
    const from = transformRef.current
    const startTime = performance.now()
    const tick = (now: number) => {
      const progress = Math.min(1, (now - startTime) / 320)
      const eased = 1 - (1 - progress) ** 3
      updateTransform({
        x: from.x + (next.x - from.x) * eased,
        y: from.y + (next.y - from.y) * eased,
        scale: from.scale + (next.scale - from.scale) * eased,
      })
      if (progress < 1) animationFrame.current = requestAnimationFrame(tick)
      else animationFrame.current = null
    }
    animationFrame.current = requestAnimationFrame(tick)
  }, [stopAnimation, updateTransform])

  const focusNode = useCallback((id: string, animate = true) => {
    const node = nodes.get(id)
    const svg = svgRef.current
    if (!node || !svg) return
    const bounds = svg.getBoundingClientRect()
    const scale = Math.min(0.58, Math.max(0.28, Math.min(bounds.width / 1450, bounds.height / 1300)))
    const point = center(node.geometry)
    const next = {
      x: (bounds.width > 900 ? bounds.width * 0.42 : bounds.width / 2) - point.x * scale,
      y: bounds.height / 2 - point.y * scale,
      scale,
    }
    if (animate) animateTo(next)
    else updateTransform(next)
  }, [animateTo, nodes, updateTransform])

  const selectNode = useCallback((id: string, fromHistory = false) => {
    if (!nodes.has(id) || id === roadmap.start.id) return
    setSelectedId(id)
    focusNode(id)
    if (!fromHistory && window.location.hash !== `#${id}`) window.history.pushState(null, '', `#${id}`)
  }, [focusNode, nodes])

  useEffect(() => {
    const svg = svgRef.current
    if (!svg) return
    const updateViewport = (width: number, height: number) => {
      if (width <= 0 || height <= 0) return
      if (!hasInitialized.current) {
        hasInitialized.current = true
        updateTransform(initialTransform(width, height))
        const deepLinkedNode = hashNodeId()
        if (deepLinkedNode && !initialDeepLinkScheduled.current) {
          initialDeepLinkScheduled.current = true
          requestAnimationFrame(() => focusNode(deepLinkedNode))
        }
      }
    }
    const bounds = svg.getBoundingClientRect()
    updateViewport(bounds.width, bounds.height)
    const observer = new ResizeObserver(([entry]) => updateViewport(entry.contentRect.width, entry.contentRect.height))
    observer.observe(svg)
    return () => observer.disconnect()
  }, [focusNode, updateTransform])

  useEffect(() => {
    const onHashChange = () => {
      const id = hashNodeId()
      setSelectedId(id)
      if (id) focusNode(id)
    }
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [focusNode])

  useEffect(() => () => stopAnimation(), [stopAnimation])

  const localPoint = (event: PointerEvent<SVGSVGElement> | WheelEvent<SVGSVGElement>): Point => {
    const bounds = event.currentTarget.getBoundingClientRect()
    return { x: event.clientX - bounds.left, y: event.clientY - bounds.top }
  }

  const beginPointer = (event: PointerEvent<SVGSVGElement>) => {
    stopAnimation()
    event.currentTarget.setPointerCapture(event.pointerId)
    pointers.current.set(event.pointerId, localPoint(event))
    const active = [...pointers.current.values()]
    if (active.length === 1) {
      gesture.current = { origin: transformRef.current, start: active[0] }
    } else if (active.length === 2) {
      const middle = midpoint(active[0], active[1])
      const current = transformRef.current
      gesture.current = {
        origin: current,
        start: middle,
        startDistance: distance(active[0], active[1]),
        worldAnchor: { x: (middle.x - current.x) / current.scale, y: (middle.y - current.y) / current.scale },
      }
    }
  }

  const movePointer = (event: PointerEvent<SVGSVGElement>) => {
    if (!pointers.current.has(event.pointerId)) return
    pointers.current.set(event.pointerId, localPoint(event))
    const active = [...pointers.current.values()]
    const currentGesture = gesture.current
    if (active.length === 1) {
      const next = { ...currentGesture.origin, x: currentGesture.origin.x + active[0].x - currentGesture.start.x, y: currentGesture.origin.y + active[0].y - currentGesture.start.y }
      updateTransform(next)
    } else if (active.length >= 2 && currentGesture.startDistance && currentGesture.worldAnchor) {
      const middle = midpoint(active[0], active[1])
      const scale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, currentGesture.origin.scale * distance(active[0], active[1]) / currentGesture.startDistance))
      updateTransform({ x: middle.x - currentGesture.worldAnchor.x * scale, y: middle.y - currentGesture.worldAnchor.y * scale, scale })
    }
  }

  const endPointer = (event: PointerEvent<SVGSVGElement>) => {
    pointers.current.delete(event.pointerId)
    const active = [...pointers.current.values()]
    if (active.length === 1) gesture.current = { origin: transformRef.current, start: active[0] }
  }

  const zoomAt = (point: Point, factor: number) => {
    stopAnimation()
    const current = transformRef.current
    const scale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, current.scale * factor))
    updateTransform({ x: point.x - ((point.x - current.x) / current.scale) * scale, y: point.y - ((point.y - current.y) / current.scale) * scale, scale })
  }

  const selectedTopic = selectedId ? topicsById.get(selectedId) ?? null : null
  const selectedGroup = selectedId ? groupsByHubId.get(selectedId) ?? null : null
  const prerequisiteTopics = selectedTopic ? roadmap.prerequisiteEdges
    .filter((edge) => edge.target === selectedTopic.id && edge.source !== 'START')
    .map((edge) => topicsById.get(edge.source)).filter((topic): topic is Topic => Boolean(topic)) : []
  const nextTopics = selectedTopic ? roadmap.prerequisiteEdges
    .filter((edge) => edge.source === selectedTopic.id)
    .map((edge) => topicsById.get(edge.target)).filter((topic): topic is Topic => Boolean(topic)) : []
  const visibleContext = useMemo(() => {
    if (!selectedId) return new Set<string>()
    const ids = new Set([selectedId])
    roadmap.visibleEdges.filter((edge) => edge.source === selectedId || edge.target === selectedId).forEach((edge) => {
      ids.add(edge.source)
      ids.add(edge.target)
    })
    return ids
  }, [selectedId])

  const closePanel = () => {
    setSelectedId(null)
    if (window.location.hash) window.history.pushState(null, '', `${window.location.pathname}${window.location.search}`)
  }
  const dismissHint = () => {
    window.localStorage.setItem('roadmap-onboarding-dismissed', '1')
    setHintVisible(false)
  }

  return (
    <main className="roadmap-app">
      <header className="floating-header">
        <h1>Robotics Control Roadmap</h1>
        <a href={REPOSITORY_URL} target="_blank" rel="noreferrer">Repository <span aria-hidden="true">↗</span></a>
      </header>
      <svg
        ref={svgRef}
        className="roadmap-canvas"
        role="application"
        aria-label="Interactive robotics control roadmap. Drag to pan, scroll or pinch to zoom, and select a topic for details."
        onPointerDown={beginPointer}
        onPointerMove={movePointer}
        onPointerUp={endPointer}
        onPointerCancel={endPointer}
        onWheel={(event) => {
          event.preventDefault()
          zoomAt(localPoint(event), Math.exp(-event.deltaY * 0.0015))
        }}
      >
        <defs>
          {roadmap.groups.map((group) => <marker key={group.id} id={`arrow-${group.id}`} markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M 0 0 L 10 5 L 0 10 z" fill={group.stroke} /></marker>)}
        </defs>
        <g transform={`translate(${transform.x} ${transform.y}) scale(${transform.scale})`}>
          <rect className="map-background" width={roadmap.canvas.width} height={roadmap.canvas.height} fill={roadmap.canvas.background} />
          {roadmap.rings.map((ring) => <ellipse key={ring.id} cx={ring.geometry.x + ring.geometry.width / 2} cy={ring.geometry.y + ring.geometry.height / 2} rx={ring.geometry.width / 2} ry={ring.geometry.height / 2} fill="none" stroke={ring.style.strokeColor ?? '#9aa0a6'} strokeWidth={numberStyle(ring.style, 'strokeWidth', 1) * 2} opacity={Math.min(1, numberStyle(ring.style, 'opacity', 20) / 100 * 0.7)} />)}
          <g className="map-edges">
            {roadmap.visibleEdges.map((edge) => {
              const path = edgePath(edge, nodes)
              if (!path) return null
              const source = nodes.get(edge.source)!
              const target = nodes.get(edge.target)!
              const groupId = target.groupId ?? source.groupId
              const group = groupId ? groupById.get(groupId) : undefined
              const isSpoke = source.kind === 'start' && target.kind === 'hub'
              const isRoot = source.kind === 'hub' && target.kind === 'topic'
              const related = !selectedId || edge.source === selectedId || edge.target === selectedId
              const baseWidth = numberStyle(edge.style, 'strokeWidth', isSpoke ? 5 : 2) * (isSpoke ? 1.6 : 1.2)
              const baseOpacity = numberStyle(edge.style, 'opacity', isSpoke ? 18 : isRoot ? 55 : 72) / 100 * (isSpoke ? 2 / 3 : isRoot ? 48 / 55 : 1)
              return <path key={edge.id} d={path} fill="none" stroke={edge.style.strokeColor ?? group?.stroke ?? '#555'} strokeWidth={baseWidth} opacity={related ? baseOpacity : baseOpacity * 0.14} markerEnd={isSpoke ? undefined : `url(#arrow-${groupId})`} />
            })}
          </g>
          <StartNode node={roadmap.start} dimmed={Boolean(selectedId) && !visibleContext.has('START')} />
          {roadmap.groups.map((group) => <MapNode key={group.hub.id} node={group.hub} selected={group.hub.id === selectedId} dimmed={Boolean(selectedId) && !visibleContext.has(group.hub.id)} onSelect={selectNode} />)}
          {roadmap.topics.map((topic) => <MapNode key={topic.id} node={topic} selected={topic.id === selectedId} dimmed={Boolean(selectedId) && !visibleContext.has(topic.id)} onSelect={selectNode} />)}
        </g>
      </svg>
      {hintVisible && !selectedId && <div className="onboarding" role="status"><span>Drag to explore · Scroll or pinch to zoom · Select a topic</span><button onClick={dismissHint} aria-label="Dismiss exploration hint">×</button></div>}
      {selectedTopic && <TopicPanel topic={selectedTopic} prerequisites={prerequisiteTopics} nextTopics={nextTopics} onNavigate={selectNode} onClose={closePanel} />}
      {selectedGroup && <CoreTrackPanel group={selectedGroup} onClose={closePanel} />}
    </main>
  )
}
