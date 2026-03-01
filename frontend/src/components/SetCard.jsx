import { useState } from 'react';
import { Heart, Bookmark, Package, Calendar, Layers, Check, ChevronLeft } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { cn } from '../lib/utils';
import api from '../api/api_test';
import { useAuth } from '../context/AuthContext';

export default function SetCard({ set, initialFavorite = false, initialWishlisted = false }) {
  const { user } = useAuth();
  const [isFavorite, setIsFavorite] = useState(initialFavorite);
  const [isWishlisted, setIsWishlisted] = useState(initialWishlisted);
  // null | 'collection' — sous-choix actif
  const [addMode, setAddMode] = useState(null);
  // feedback bref après ajout
  const [feedback, setFeedback] = useState(null); // null | 'collection'

  function showFeedback(key) {
    setFeedback(key);
    setTimeout(() => setFeedback(null), 1800);
  }

  async function toggleFavorite(e) {
    e.stopPropagation();
    if (!user) return;
    if (isFavorite) {
      await api.delete(`/users/${user.id}/favorites/${set.set_num}`).catch(() => {});
      setIsFavorite(false);
    } else {
      await api.post(`/users/${user.id}/favorites`, { set_num: set.set_num }).catch(() => {});
      setIsFavorite(true);
    }
  }

  async function toggleWishlist(e) {
    e.stopPropagation();
    if (!user) return;
    if (isWishlisted) {
      await api.delete(`/users/${user.id}/wishlist/sets/${set.set_num}`).catch(() => {});
      setIsWishlisted(false);
    } else {
      await api.post(`/users/${user.id}/wishlist/sets`, { set_num: set.set_num }).catch(() => {});
      setIsWishlisted(true);
    }
  }

  async function addToCollection(isBuilt) {
    if (!user) return;
    await api
      .post(`/users/${user.id}/collection`, { set_num: set.set_num, is_built: isBuilt })
      .catch(() => {});
    setAddMode(null);
    showFeedback('collection');
  }

  // Le panel s'affiche via CSS group-hover + JS quand un sous-choix est actif
  const panelExpanded = addMode !== null || feedback !== null;

  return (
    <div className="group relative">
      <Card
        className={cn(
          'flex flex-col transition-all duration-200',
          'group-hover:shadow-lg group-hover:-translate-y-0.5',
        )}
      >
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

          {/* Badge coverage (BuildablePage) */}
          {set.coverage_pct != null && (
            <div className="absolute top-2 left-2">
              <span className="rounded-full bg-green-500 px-2 py-0.5 text-xs font-bold text-white">
                {set.coverage_pct}%
              </span>
            </div>
          )}
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

          {/* ── Panel d'actions hover ── */}
          {user && (
            <div
              className={cn(
                'overflow-hidden transition-[max-height,opacity] duration-200',
                panelExpanded
                  ? 'max-h-24 opacity-100'
                  : 'max-h-0 opacity-0 group-hover:max-h-24 group-hover:opacity-100',
              )}
            >
              <div className="pt-3 border-t border-gray-100">
                {feedback === 'collection' ? (
                  /* Feedback ajout collection */
                  <p className="flex items-center gap-1.5 text-sm text-green-600 font-medium">
                    <Check size={14} />
                    Ajouté à la collection
                  </p>
                ) : addMode === 'collection' ? (
                  /* Sous-choix is_built */
                  <div className="space-y-2">
                    <p className="text-xs text-gray-500 font-medium">Set déjà construit ?</p>
                    <div className="flex gap-2">
                      <Button size="sm" variant="default" className="flex-1 text-xs" onClick={() => addToCollection(true)}>
                        ✓ Oui
                      </Button>
                      <Button size="sm" variant="outline" className="flex-1 text-xs" onClick={() => addToCollection(false)}>
                        ✗ Non
                      </Button>
                      <button
                        onClick={() => setAddMode(null)}
                        className="text-gray-400 hover:text-gray-600 px-1"
                        title="Annuler"
                      >
                        <ChevronLeft size={14} />
                      </button>
                    </div>
                  </div>
                ) : (
                  /* Boutons principaux */
                  <div className="flex gap-1.5">
                    <button
                      onClick={toggleWishlist}
                      title="Wishlist"
                      className={cn(
                        'flex flex-1 items-center justify-center gap-1 rounded-md py-1.5 text-xs font-medium transition-colors',
                        isWishlisted
                          ? 'bg-blue-100 text-blue-600'
                          : 'bg-gray-100 text-gray-600 hover:bg-blue-50 hover:text-blue-600',
                      )}
                    >
                      <Bookmark size={12} fill={isWishlisted ? 'currentColor' : 'none'} />
                      Wishlist
                    </button>
                    <button
                      onClick={toggleFavorite}
                      title="Favoris"
                      className={cn(
                        'flex flex-1 items-center justify-center gap-1 rounded-md py-1.5 text-xs font-medium transition-colors',
                        isFavorite
                          ? 'bg-red-100 text-red-600'
                          : 'bg-gray-100 text-gray-600 hover:bg-red-50 hover:text-red-600',
                      )}
                    >
                      <Heart size={12} fill={isFavorite ? 'currentColor' : 'none'} />
                      Favoris
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); setAddMode('collection'); }}
                      title="Ajouter à ma collection"
                      className="flex flex-1 items-center justify-center gap-1 rounded-md py-1.5 text-xs font-medium bg-gray-100 text-gray-600 hover:bg-green-50 hover:text-green-700 transition-colors"
                    >
                      <Package size={12} />
                      Collection
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
