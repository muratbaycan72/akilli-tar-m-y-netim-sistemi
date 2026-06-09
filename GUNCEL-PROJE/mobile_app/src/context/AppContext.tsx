import React, { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { api } from '../services/api';
import type { Field } from '../types';

interface AppContextType {
  fields: Field[];
  selectedField: Field | null;
  setSelectedField: (field: Field | null) => void;
  loading: boolean;
  error: string | null;
  refreshFields: () => Promise<void>;
}

const AppContext = createContext<AppContextType>({
  fields: [],
  selectedField: null,
  setSelectedField: () => {},
  loading: true,
  error: null,
  refreshFields: async () => {},
});

export function AppProvider({ children }: { children: ReactNode }) {
  const [fields, setFields] = useState<Field[]>([]);
  const [selectedField, setSelectedField] = useState<Field | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refreshFields = async () => {
    try {
      setError(null);
      const data = await api.getFields();
      setFields(data);
      if (!selectedField && data.length > 0) {
        setSelectedField(data[0]);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Tarlalar yüklenemedi');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshFields();
  }, []);

  return (
    <AppContext.Provider
      value={{ fields, selectedField, setSelectedField, loading, error, refreshFields }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}
