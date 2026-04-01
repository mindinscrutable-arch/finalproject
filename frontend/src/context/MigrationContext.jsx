import { createContext, useContext } from 'react';

const MigrationContext = createContext();

export const useMigration = () => useContext(MigrationContext);

export const MigrationProvider = ({ children }) => {
  return (
    <MigrationContext.Provider value={{}}>
      {children}
    </MigrationContext.Provider>
  );
};