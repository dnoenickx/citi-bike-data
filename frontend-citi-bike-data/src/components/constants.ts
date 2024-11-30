import type { LngLatLike, MapOptions } from 'mapbox-gl';

export const BOTTOM_LEFT: LngLatLike = [-74.0848, 40.6304];
export const TOP_RIGHT: LngLatLike = [-73.7877, 40.8916];
export const MAP_CONFIG_DEFAULT: Partial<MapOptions> = {
  bounds: [TOP_RIGHT, BOTTOM_LEFT],
  zoom: 10,
};