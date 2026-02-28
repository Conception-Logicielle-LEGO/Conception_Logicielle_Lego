import { cn } from '../../lib/utils';

export function Label({ className, children, ...props }) {
  return (
    <label
      className={cn('text-sm font-medium leading-none text-gray-700', className)}
      {...props}
    >
      {children}
    </label>
  );
}
