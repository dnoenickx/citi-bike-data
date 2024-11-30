import { create } from 'zustand';

interface Store {
    stations: string[]
    setStations: (stations: string[]) => void
}

export const useStore = create<Store>((set) => ({
    stations: [],
    setStations: (stations) => set({ stations }),
}));