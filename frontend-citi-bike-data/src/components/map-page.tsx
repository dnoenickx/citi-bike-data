'use client';
import type { MutableRefObject } from 'react';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import mapboxgl, { Map, MapSourceDataEvent } from 'mapbox-gl';


import { MAP_CONFIG_DEFAULT } from './constants';
import { useApplyLayers } from '@/map/map-config';

if(!process.env.NEXT_PUBLIC_MAPBOX_API_KEY) {
    throw new Error("NEXT_PUBLIC_MAPBOX_API_KEY is not set in the environment variables");
}
mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_API_KEY
export const MapPage = () => {
    const map: MutableRefObject<Map | null> = useRef(null);
    const mapContainer: MutableRefObject<HTMLDivElement | null> = useRef(null);
    const [mapLoaded, setMapLoaded] = useState(false);
    const [loading, setLoading] = useState(false);
    useApplyLayers(map, mapLoaded);
    const handleIdle = useCallback(() => {
        if (loading) {
            setLoading(false);
        }
    }, [loading, setLoading]);
    const handleLoading = useCallback(
        (e: MapSourceDataEvent) => {
            // If the tile property is defined, then the event is a tile loading event. Ignore it.
            if (!loading && e.tile === undefined) {
                setLoading(true);
            }
        },
        [loading, setLoading]
    );
    useEffect(() => {
        if (map.current || !mapContainer.current) return;

        map.current = new Map({
            ...MAP_CONFIG_DEFAULT,
            container: mapContainer.current,
        });
        map.current?.on('load', async () => {
            setMapLoaded(true);
        });
    }, []);

    useEffect(() => {
        if (!map.current || !mapLoaded) return;
        map.current?.setConfigProperty('basemap', 'theme', 'monochrome');
        map.current.on('idle', handleIdle);
        map.current.on('sourcedataloading', handleLoading);

        return () => {
            map.current?.off('idle', handleIdle);
            map.current?.off('sourcedataloading', handleLoading);
        };
    }, [mapLoaded, handleIdle, handleLoading]);
    return (
        <div className='w-[100svw] h-[100svh]'><div className="h-full w-full" ref={mapContainer} ></div></div>
    );
};
