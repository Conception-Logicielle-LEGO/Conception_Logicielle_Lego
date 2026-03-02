import { cn } from '../../lib/utils';

const variants = {
  default: 'bg-red-100 text-red-700',
  secondary: 'bg-gray-100 text-gray-700',
  outline: 'border border-gray-300 text-gray-700',
  destructive: 'bg-red-500 text-white',
};

export function Badge({ className, variant = 'default', children, ...props }) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
        variants[variant],
        className,
      )}
      {...props}
    >
      {children}
    </span>
  );
}
