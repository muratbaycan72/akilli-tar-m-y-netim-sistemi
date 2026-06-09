import { createContext, useContext, useState, type ReactNode } from 'react';
import type { Field } from '../types';

interface AppContextType {
  selectedField: Field | null;
  setSelectedField: (field: Field | null) => void;
}

const AppContext = createContext<AppContextType>({
  selectedField: null,
  setSelectedField: () => {},
});

export function AppProvider({ children }: { children: ReactNode }) {
  const [selectedField, setSelectedField] = useState<Field | null>(null);
  return (
    <AppContext.Provider value={{ selectedField, setSelectedField }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  return useContext(AppContext);
}
