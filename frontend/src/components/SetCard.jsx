import { useState } from 'react';
import { Heart, Bookmark, Package, Calendar, Layers } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { cn } from '../lib/utils';

export default function SetCard({ set }) {
  const [isFavorite, setIsFavorite] = useState(false);
  const [isWishlisted, setIsWishlisted] = useState(false);

  return (
    <Card className="flex flex-col transition-shadow hover:shadow-md">
      {/* Image ou placeholder */}
      <div className="relative h-40 overflow-hidden rounded-t-xl bg-gray-100">
        {set.img_url ? (
          <img
            src={set.img_url}
            alt={set.name}
            className="h-full w-full object-contain p-2"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-gray-300">
            <Layers size={48} />
          </div>
        )}

        {/* Boutons favoris / wishlist */}
        <div className="absolute top-2 right-2 flex gap-1">
          <button
            onClick={() => setIsWishlisted((v) => !v)}
            className={cn(
              'rounded-full bg-white/90 p-1.5 shadow transition-colors hover:bg-white',
              isWishlisted ? 'text-blue-500' : 'text-gray-400',
            )}
            title="Ajouter à la wishlist"
          >
            <Bookmark size={14} fill={isWishlisted ? 'currentColor' : 'none'} />
          </button>
          <button
            onClick={() => setIsFavorite((v) => !v)}
            className={cn(
              'rounded-full bg-white/90 p-1.5 shadow transition-colors hover:bg-white',
              isFavorite ? 'text-red-500' : 'text-gray-400',
            )}
            title="Ajouter aux favoris"
          >
            <Heart size={14} fill={isFavorite ? 'currentColor' : 'none'} />
          </button>
        </div>
      </div>

      <CardContent className="flex flex-1 flex-col gap-2 p-4">
        <h3 className="font-semibold text-gray-900 leading-snug line-clamp-2">{set.name}</h3>

        <div className="flex flex-wrap gap-1.5 mt-auto pt-2">
          <Badge variant="outline" className="flex items-center gap-1 text-xs">
            <span className="font-mono text-red-600">#{set.set_num}</span>
          </Badge>
          {set.year && (
            <Badge variant="secondary" className="flex items-center gap-1 text-xs">
              <Calendar size={10} />
              {set.year}
            </Badge>
          )}
          {set.num_parts != null && (
            <Badge variant="secondary" className="flex items-center gap-1 text-xs">
              <Package size={10} />
              {set.num_parts} pièces
            </Badge>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
