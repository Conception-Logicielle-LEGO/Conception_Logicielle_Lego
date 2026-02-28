import { createContext, useContext, useState } from 'react';
import { cn } from '../../lib/utils';

const TabsContext = createContext(null);

export function Tabs({ defaultValue, value, onValueChange, className, children }) {
  const [internalValue, setInternalValue] = useState(defaultValue);
  const active = value ?? internalValue;

  function handleChange(v) {
    setInternalValue(v);
    onValueChange?.(v);
  }

  return (
    <TabsContext.Provider value={{ active, onChange: handleChange }}>
      <div className={cn('w-full', className)}>{children}</div>
    </TabsContext.Provider>
  );
}

export function TabsList({ className, children }) {
  return (
    <div
      className={cn(
        'inline-flex h-10 items-center justify-center rounded-md bg-gray-100 p-1 text-gray-500',
        className,
      )}
    >
      {children}
    </div>
  );
}

export function TabsTrigger({ value, className, children }) {
  const { active, onChange } = useContext(TabsContext);
  const isActive = active === value;

  return (
    <button
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium transition-all cursor-pointer',
        isActive
          ? 'bg-white text-gray-900 shadow-sm'
          : 'text-gray-500 hover:text-gray-700',
        className,
      )}
      onClick={() => onChange(value)}
      type="button"
    >
      {children}
    </button>
  );
}

export function TabsContent({ value, className, children }) {
  const { active } = useContext(TabsContext);
  if (active !== value) return null;
  return <div className={cn('mt-4', className)}>{children}</div>;
}
