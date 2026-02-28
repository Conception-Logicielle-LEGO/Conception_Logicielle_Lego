import { Package } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';

const colorMap = {
  Red: 'bg-red-400',
  Blue: 'bg-blue-400',
  Yellow: 'bg-yellow-400',
  Green: 'bg-green-400',
  White: 'bg-gray-100 border border-gray-300',
  Black: 'bg-gray-900',
  'Light Grey': 'bg-gray-300',
  'Dark Grey': 'bg-gray-500',
};

export default function PieceCard({ part }) {
  const colorClass = colorMap[part.color] || 'bg-gray-200';

  return (
    <Card className="transition-shadow hover:shadow-md">
      <CardContent className="p-4">
        <div className="flex items-start gap-3">
          {/* Swatch couleur ou icône */}
          <div
            className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-lg ${colorClass}`}
          >
            {!colorMap[part.color] && <Package size={20} className="text-gray-500" />}
          </div>

          <div className="flex-1 min-w-0">
            <p className="font-medium text-gray-900 truncate">{part.name}</p>
            <p className="text-xs text-gray-500 mt-0.5">#{part.part_num}</p>
            <div className="mt-2 flex items-center gap-2">
              <Badge variant="secondary">{part.color}</Badge>
              <span className="text-xs text-gray-500">x{part.quantity}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
