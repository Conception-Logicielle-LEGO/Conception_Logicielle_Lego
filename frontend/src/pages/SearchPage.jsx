import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import api from '../api/api_test';
import { mockParts, themes, colors } from '../data/mockData';
import SetCard from '../components/SetCard';
import PieceCard from '../components/PieceCard';
import Loader from '../components/Loader';
import { Input } from '../components/ui/input';
import { Select } from '../components/ui/select';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../components/ui/tabs';

export default function SearchPage() {
  const [tab, setTab] = useState('sets');

  // Sets state
  const [allSets, setAllSets] = useState([]);
  const [setsLoading, setSetsLoading] = useState(true);
  const [setQuery, setSetQuery] = useState('');
  const [selectedTheme, setSelectedTheme] = useState('');

  // Parts state
  const [partQuery, setPartQuery] = useState('');
  const [selectedColor, setSelectedColor] = useState('');

  useEffect(() => {
    api.get('/sets/recent')
      .then((r) => setAllSets(r.data))
      .catch(() => setAllSets([]))
      .finally(() => setSetsLoading(false));
  }, []);

  const filteredSets = allSets.filter((s) => {
    const q = setQuery.toLowerCase();
    const matchQuery =
      !q || s.name?.toLowerCase().includes(q) || s.set_num?.toLowerCase().includes(q);
    const matchTheme = !selectedTheme || s.theme_id === Number(selectedTheme);
    return matchQuery && matchTheme;
  });

  const filteredParts = mockParts.filter((p) => {
    const q = partQuery.toLowerCase();
    const matchQuery =
      !q || p.name.toLowerCase().includes(q) || p.part_num.toLowerCase().includes(q);
    const matchColor = !selectedColor || p.color === selectedColor;
    return matchQuery && matchColor;
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Recherche</h1>
        <p className="mt-1 text-gray-500">Cherchez des sets ou des pièces LEGO</p>
      </div>

      <Tabs value={tab} onValueChange={setTab}>
        <TabsList>
          <TabsTrigger value="sets">Sets</TabsTrigger>
          <TabsTrigger value="parts">Pièces</TabsTrigger>
        </TabsList>

        {/* ── SETS ── */}
        <TabsContent value="sets">
          <div className="mb-4 flex flex-col gap-3 sm:flex-row">
            <div className="relative flex-1">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <Input
                placeholder="Nom ou numéro de set…"
                className="pl-9"
                value={setQuery}
                onChange={(e) => setSetQuery(e.target.value)}
              />
            </div>
            <Select
              className="sm:w-48"
              value={selectedTheme}
              onChange={(e) => setSelectedTheme(e.target.value)}
            >
              {themes.map((t) => (
                <option key={t.id} value={t.id === 1 ? '' : t.id}>
                  {t.name}
                </option>
              ))}
            </Select>
          </div>

          {setsLoading ? (
            <Loader message="Chargement des sets…" />
          ) : filteredSets.length === 0 ? (
            <p className="py-12 text-center text-gray-500">Aucun set trouvé.</p>
          ) : (
            <>
              <p className="mb-3 text-sm text-gray-500">{filteredSets.length} set(s)</p>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {filteredSets.map((set) => (
                  <SetCard key={set.set_num} set={set} />
                ))}
              </div>
            </>
          )}
        </TabsContent>

        {/* ── PIÈCES ── */}
        <TabsContent value="parts">
          <div className="mb-4 flex flex-col gap-3 sm:flex-row">
            <div className="relative flex-1">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <Input
                placeholder="Nom ou numéro de pièce…"
                className="pl-9"
                value={partQuery}
                onChange={(e) => setPartQuery(e.target.value)}
              />
            </div>
            <Select
              className="sm:w-48"
              value={selectedColor}
              onChange={(e) => setSelectedColor(e.target.value)}
            >
              {colors.map((c) => (
                <option key={c.id} value={c.id === 1 ? '' : c.name}>
                  {c.name}
                </option>
              ))}
            </Select>
          </div>

          {filteredParts.length === 0 ? (
            <p className="py-12 text-center text-gray-500">Aucune pièce trouvée.</p>
          ) : (
            <>
              <p className="mb-3 text-sm text-gray-500">{filteredParts.length} pièce(s)</p>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {filteredParts.map((part) => (
                  <PieceCard key={part.part_num} part={part} />
                ))}
              </div>
            </>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
