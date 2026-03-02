import { useState } from 'react';
import { Package, Bookmark, Check, ChevronLeft } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { cn } from '../lib/utils';
import api from '../api/api_test';
import { useAuth } from '../context/AuthContext';

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
  const { user } = useAuth();
  const colorClass = colorMap[part.color] || 'bg-gray-200';
  const colorId = part.color_id ?? 0;

  // null | 'owned' | 'wishlist'
  const [addMode, setAddMode] = useState(null);
  const [feedback, setFeedback] = useState(null); // null | 'wishlist' | 'owned'

  // owned form
  const [qtyLibre, setQtyLibre] = useState(0);
  const [qtyUsed, setQtyUsed] = useState(0);

  // wishlist form
  const [qtyWish, setQtyWish] = useState(1);

  function showFeedback(key) {
    setFeedback(key);
    setTimeout(() => setFeedback(null), 1800);
  }

  function resetOwnedForm() {
    setQtyLibre(0);
    setQtyUsed(0);
    setAddMode(null);
  }

  async function addToOwned() {
    if (!user) return;
    const posts = [];
    if (qtyLibre > 0) {
      posts.push(
        api.post(`/users/${user.id}/parts`, {
          part_num: part.part_num,
          color_id: colorId,
          quantity: qtyLibre,
          is_used: false,
        }).catch(() => {})
      );
    }
    if (qtyUsed > 0) {
      posts.push(
        api.post(`/users/${user.id}/parts`, {
          part_num: part.part_num,
          color_id: colorId,
          quantity: qtyUsed,
          is_used: true,
        }).catch(() => {})
      );
    }
    if (posts.length === 0) return;
    await Promise.all(posts);
    resetOwnedForm();
    showFeedback('owned');
  }

  async function addToWishlist() {
    if (!user) return;
    await api
      .post(`/users/${user.id}/wishlist/parts`, {
        part_num: part.part_num,
        color_id: colorId,
        quantity: qtyWish,
      })
      .catch(() => {});
    setQtyWish(1);
    setAddMode(null);
    showFeedback('wishlist');
  }

  const panelExpanded = addMode !== null || feedback !== null;

  return (
    <div className="group relative">
      <Card
        className={cn(
          'transition-all duration-200',
          'group-hover:shadow-lg group-hover:-translate-y-0.5',
        )}
      >
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            {/* Image de la pièce ou swatch couleur */}
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg overflow-hidden bg-gray-100">
              {part.img_url ? (
                <img
                  src={part.img_url}
                  alt={part.name}
                  className="h-full w-full object-contain"
                  onError={(e) => { e.currentTarget.style.display = 'none'; e.currentTarget.nextSibling.style.display = 'flex'; }}
                />
              ) : null}
              <div
                className={`${part.img_url ? 'hidden' : ''} flex h-full w-full items-center justify-center ${colorClass}`}
              >
                {!colorMap[part.color] && <Package size={20} className="text-gray-500" />}
              </div>
            </div>

            <div className="flex-1 min-w-0">
              <p className="font-medium text-gray-900 truncate">{part.name}</p>
              <p className="text-xs text-gray-500 mt-0.5">#{part.part_num}</p>
              <div className="mt-2 flex items-center gap-2">
                {part.color && <Badge variant="secondary">{part.color}</Badge>}
                {part.quantity != null && (
                  <span className="text-xs text-gray-500">x{part.quantity}</span>
                )}
              </div>
            </div>
          </div>

          {/* ── Panel d'actions hover ── */}
          {user && (
            <div
              className={cn(
                'overflow-hidden transition-[max-height,opacity] duration-200',
                panelExpanded
                  ? 'max-h-32 opacity-100'
                  : 'max-h-0 opacity-0 group-hover:max-h-32 group-hover:opacity-100',
              )}
            >
              <div className="pt-3 mt-3 border-t border-gray-100">
                {feedback === 'wishlist' ? (
                  <p className="flex items-center gap-1.5 text-sm text-blue-600 font-medium">
                    <Check size={14} />
                    Ajouté à la wishlist
                  </p>
                ) : feedback === 'owned' ? (
                  <p className="flex items-center gap-1.5 text-sm text-green-600 font-medium">
                    <Check size={14} />
                    Ajouté à mes pièces
                  </p>
                ) : addMode === 'owned' ? (
                  /* Formulaire quantités libres / utilisées */
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <label className="text-xs text-gray-500 w-16 shrink-0">Libres</label>
                      <input
                        type="number"
                        min="0"
                        value={qtyLibre}
                        onChange={(e) => setQtyLibre(Math.max(0, parseInt(e.target.value) || 0))}
                        className="w-16 rounded border border-gray-200 px-1.5 py-0.5 text-xs text-center focus:outline-none focus:ring-1 focus:ring-green-400"
                      />
                      <label className="text-xs text-gray-500 w-16 shrink-0">Utilisées</label>
                      <input
                        type="number"
                        min="0"
                        value={qtyUsed}
                        onChange={(e) => setQtyUsed(Math.max(0, parseInt(e.target.value) || 0))}
                        className="w-16 rounded border border-gray-200 px-1.5 py-0.5 text-xs text-center focus:outline-none focus:ring-1 focus:ring-green-400"
                      />
                    </div>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="default"
                        className="flex-1 text-xs"
                        onClick={addToOwned}
                        disabled={qtyLibre === 0 && qtyUsed === 0}
                      >
                        Ajouter
                      </Button>
                      <button
                        onClick={resetOwnedForm}
                        className="text-gray-400 hover:text-gray-600 px-1"
                        title="Annuler"
                      >
                        <ChevronLeft size={14} />
                      </button>
                    </div>
                  </div>
                ) : addMode === 'wishlist' ? (
                  /* Formulaire quantité wishlist */
                  <div className="flex items-center gap-2">
                    <label className="text-xs text-gray-500 shrink-0">Quantité</label>
                    <input
                      type="number"
                      min="1"
                      value={qtyWish}
                      onChange={(e) => setQtyWish(Math.max(1, parseInt(e.target.value) || 1))}
                      className="w-16 rounded border border-gray-200 px-1.5 py-0.5 text-xs text-center focus:outline-none focus:ring-1 focus:ring-blue-400"
                    />
                    <Button
                      size="sm"
                      variant="outline"
                      className="text-xs"
                      onClick={addToWishlist}
                    >
                      <Check size={12} />
                    </Button>
                    <button
                      onClick={() => { setQtyWish(1); setAddMode(null); }}
                      className="text-gray-400 hover:text-gray-600 px-1"
                      title="Annuler"
                    >
                      <ChevronLeft size={14} />
                    </button>
                  </div>
                ) : (
                  /* Boutons principaux */
                  <div className="flex gap-1.5">
                    <button
                      onClick={(e) => { e.stopPropagation(); setAddMode('wishlist'); }}
                      className="flex flex-1 items-center justify-center gap-1 rounded-md py-1.5 text-xs font-medium bg-gray-100 text-gray-600 hover:bg-blue-50 hover:text-blue-600 transition-colors"
                    >
                      <Bookmark size={12} />
                      Wishlist
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); setAddMode('owned'); }}
                      className="flex flex-1 items-center justify-center gap-1 rounded-md py-1.5 text-xs font-medium bg-gray-100 text-gray-600 hover:bg-green-50 hover:text-green-700 transition-colors"
                    >
                      <Package size={12} />
                      Mes pièces
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
