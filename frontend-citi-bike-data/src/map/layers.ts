import { LayerSpecification } from "mapbox-gl";
import { STATION_SOURCE_ID } from "./sources";

export const STATION_LAYER: LayerSpecification = {
    id: STATION_SOURCE_ID,
    source: STATION_SOURCE_ID,
    type: 'circle',
    
};