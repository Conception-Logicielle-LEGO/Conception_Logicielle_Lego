import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Heart, Bookmark, User, Package, Hammer, Box, Trash2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../components/ui/tabs';
import SetCard from '../components/SetCard';
import Loader from '../components/Loader';
import api from '../api/api_test';

export default function AccountPage() {
  const { user, isLoading } = useAuth();
  const navigate = useNavigate();

  const [collection, setCollection] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [wishlistSets, setWishlistSets] = useState([]);
  const [wishlistParts, setWishlistParts] = useState([]);
  const [ownedParts, setOwnedParts] = useState([]);
  const [dataLoading, setDataLoading] = useState(false);

  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login', { replace: true });
    }
  }, [user, isLoading, navigate]);

  useEffect(() => {
    if (!user) return;
    const id = user.id;
    setDataLoading(true);
    Promise.all([
      api.get(`/users/${id}/collection`).then((r) => r.data).catch(() => []),
      api.get(`/users/${id}/favorites`).then((r) => r.data).catch(() => []),
      api.get(`/users/${id}/wishlist/sets`).then((r) => r.data).catch(() => []),
      api.get(`/users/${id}/wishlist/parts`).then((r) => r.data).catch(() => []),
      api.get(`/users/${id}/parts`).then((r) => r.data).catch(() => []),
    ]).then(([col, fav, wSets, wParts, parts]) => {
      setCollection(col);
      setFavorites(fav);
      setWishlistSets(wSets);
      setWishlistParts(wParts);
      setOwnedParts(parts);
    }).finally(() => setDataLoading(false));
  }, [user]);

  // Groupe les lignes (libre/utilisée) par (part_num, color_id)
  const groupedParts = Object.values(
    ownedParts.reduce((acc, row) => {
      const key = `${row.part_num}-${row.color_id}`;
      if (!acc[key]) {
        acc[key] = {
          part_num: row.part_num,
          color_id: row.color_id,
          name: row.name ?? row.part_num,
          img_url: row.img_url ?? null,
          qty_libre: 0,
          qty_used: 0,
        };
      }
      if (row.is_used) acc[key].qty_used += row.quantity;
      else acc[key].qty_libre += row.quantity;
      return acc;
    }, {})
  );

  if (isLoading) return null;
  if (!user) return null;

  return (
    <div className="space-y-8">
      {/* En-tête compte */}
      <div className="flex items-center gap-4">
        <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-100">
          <User size={28} className="text-red-600" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{user.username}</h1>
          <p className="text-gray-500">{user.email}</p>
        </div>
      </div>

      {dataLoading ? (
        <Loader message="Chargement de votre compte…" />
      ) : (
        <div className="space-y-8">
          {/* Ma collection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package size={18} className="text-gray-600" />
                Ma collection ({collection.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              {collection.length === 0 ? (
                <p className="py-6 text-center text-sm text-gray-500">
                  Votre collection est vide.
                </p>
              ) : (
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {collection.map((item) => (
                    <div key={item.set_num} className="flex flex-col gap-1">
                      <SetCard set={item} />
                      <div className="flex gap-1">
                        <button
                          onClick={async () => {
                            const newBuilt = !item.is_built;
                            await api.put(`/users/${user.id}/collection/${item.set_num}/built`, { is_built: newBuilt }).catch(() => {});
                            setCollection((prev) =>
                              prev.map((s) => s.set_num === item.set_num ? { ...s, is_built: newBuilt } : s)
                            );
                          }}
                          className={`flex flex-1 items-center justify-center gap-1.5 rounded-md py-1.5 text-xs font-medium transition-colors ${
                            item.is_built
                              ? 'bg-green-100 text-green-700 hover:bg-yellow-50 hover:text-yellow-700'
                              : 'bg-gray-100 text-gray-500 hover:bg-green-50 hover:text-green-700'
                          }`}
                        >
                          {item.is_built ? <><Hammer size={12} /> Construit</> : <><Box size={12} /> Non construit</>}
                        </button>
                        <button
                          onClick={async () => {
                            await api.delete(`/users/${user.id}/collection/${item.set_num}`).catch(() => {});
                            setCollection((prev) => prev.filter((s) => s.set_num !== item.set_num));
                          }}
                          title="Retirer de la collection"
                          className="flex items-center justify-center rounded-md px-2 py-1.5 text-xs text-gray-400 hover:bg-red-50 hover:text-red-600 transition-colors"
                        >
                          <Trash2 size={13} />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Mes pièces */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package size={18} className="text-green-600" />
                Mes pièces ({groupedParts.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              {groupedParts.length === 0 ? (
                <p className="py-6 text-center text-sm text-gray-500">
                  Vous n'avez pas encore de pièces.
                  <br />
                  Cherchez des pièces et ajoutez-les depuis la recherche.
                </p>
              ) : (
                <ul className="divide-y divide-gray-100">
                  {groupedParts.map((p) => (
                    <li
                      key={`${p.part_num}-${p.color_id}`}
                      className="flex items-center justify-between py-2.5 text-sm"
                    >
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded overflow-hidden bg-gray-100">
                        {p.img_url ? (
                          <img src={p.img_url} alt={p.name} className="h-full w-full object-contain" />
                        ) : (
                          <Package size={16} className="text-gray-400" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <span className="font-medium text-gray-800 truncate block">{p.name}</span>
                        <span className="text-xs text-gray-500">#{p.part_num} — Couleur #{p.color_id}</span>
                      </div>
                      <div className="flex items-center gap-3 shrink-0 ml-3">
                        <span className="text-xs text-gray-500">
                          {p.qty_libre > 0 && <span>{p.qty_libre} libre{p.qty_libre > 1 ? 's' : ''}</span>}
                          {p.qty_libre > 0 && p.qty_used > 0 && <span> / </span>}
                          {p.qty_used > 0 && <span>{p.qty_used} utilisée{p.qty_used > 1 ? 's' : ''}</span>}
                        </span>
                        <button
                          onClick={async () => {
                            await api.delete(`/users/${user.id}/parts/${p.part_num}/${p.color_id}`).catch(() => {});
                            setOwnedParts((prev) =>
                              prev.filter((r) => !(r.part_num === p.part_num && r.color_id === p.color_id))
                            );
                          }}
                          title="Supprimer"
                          className="flex items-center justify-center rounded-md px-1.5 py-1 text-gray-400 hover:bg-red-50 hover:text-red-600 transition-colors"
                        >
                          <Trash2 size={13} />
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>

          {/* Favoris */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Heart size={18} className="text-red-500" />
                Mes favoris ({favorites.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              {favorites.length === 0 ? (
                <p className="py-6 text-center text-sm text-gray-500">
                  Vous n'avez pas encore de favoris.
                  <br />
                  Cliquez sur ❤ sur un set pour l'ajouter.
                </p>
              ) : (
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {favorites.map((fav) => (
                    <SetCard
                      key={fav.set_num}
                      set={fav}
                      initialFavorite={true}
                    />
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Wishlist */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bookmark size={18} className="text-blue-500" />
                Ma wishlist
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="sets">
                <TabsList>
                  <TabsTrigger value="sets">Sets ({wishlistSets.length})</TabsTrigger>
                  <TabsTrigger value="parts">Pièces ({wishlistParts.length})</TabsTrigger>
                </TabsList>

                <TabsContent value="sets">
                  {wishlistSets.length === 0 ? (
                    <p className="py-6 text-center text-sm text-gray-500">
                      Votre wishlist est vide.
                      <br />
                      Cliquez sur 🔖 sur un set pour l'ajouter.
                    </p>
                  ) : (
                    <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                      {wishlistSets.map((item) => (
                        <SetCard
                          key={item.set_num}
                          set={item}
                          initialWishlisted={true}
                        />
                      ))}
                    </div>
                  )}
                </TabsContent>

                <TabsContent value="parts">
                  {wishlistParts.length === 0 ? (
                    <p className="py-6 text-center text-sm text-gray-500">
                      Aucune pièce dans votre wishlist.
                    </p>
                  ) : (
                    <ul className="mt-4 divide-y divide-gray-100">
                      {wishlistParts.map((part) => (
                        <li
                          key={`${part.part_num}-${part.color_id}`}
                          className="flex items-center justify-between py-2 text-sm"
                        >
                          <span className="font-mono text-gray-700">{part.part_num}</span>
                          <span className="text-gray-500">Couleur #{part.color_id}</span>
                          <span className="font-medium">x{part.quantity}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
