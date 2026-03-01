import { useState, useEffect, useRef } from 'react';
import { Search } from 'lucide-react';
import api from '../api/api_test';
import { colors } from '../data/mockData';
import SetCard from '../components/SetCard';
import PieceCard from '../components/PieceCard';
import Loader from '../components/Loader';
import { Input } from '../components/ui/input';
import { Select } from '../components/ui/select';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../components/ui/tabs';

function useDebounce(value, delay = 400) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return debounced;
}

export default function SearchPage() {
  const [tab, setTab] = useState('sets');

  // Sets state
  const [sets, setSets] = useState([]);
  const [setsLoading, setSetsLoading] = useState(false);
  const [setQuery, setSetQuery] = useState('');
  const [selectedTheme, setSelectedTheme] = useState('');
  const debouncedSetQuery = useDebounce(setQuery);
  const debouncedTheme = useDebounce(selectedTheme);

  // Parts state
  const [parts, setParts] = useState([]);
  const [partsLoading, setPartsLoading] = useState(false);
  const [partQuery, setPartQuery] = useState('');
  const [selectedColor, setSelectedColor] = useState('');
  const debouncedPartQuery = useDebounce(partQuery);
  const debouncedColor = useDebounce(selectedColor);

  // Chargement initial des sets récents
  const initialLoad = useRef(false);
  useEffect(() => {
    if (initialLoad.current) return;
    initialLoad.current = true;
    setSetsLoading(true);
    api
      .get('/sets/recent')
      .then((r) => setSets(r.data))
      .catch(() => setSets([]))
      .finally(() => setSetsLoading(false));
  }, []);

  // Recherche sets (déclenché par debounce)
  useEffect(() => {
    if (!debouncedSetQuery && !debouncedTheme) return;
    setSetsLoading(true);
    const params = { q: debouncedSetQuery, limit: 40 };
    if (debouncedTheme) params.theme_id = debouncedTheme;
    api
      .get('/sets/search', { params })
      .then((r) => setSets(r.data))
      .catch(() => setSets([]))
      .finally(() => setSetsLoading(false));
  }, [debouncedSetQuery, debouncedTheme]);

  // Recherche pièces
  useEffect(() => {
    if (!debouncedPartQuery && !debouncedColor) return;
    setPartsLoading(true);
    const params = { q: debouncedPartQuery, limit: 40 };
    if (debouncedColor) params.color_id = debouncedColor;
    api
      .get('/parts/search', { params })
      .then((r) => setParts(r.data))
      .catch(() => setParts([]))
      .finally(() => setPartsLoading(false));
  }, [debouncedPartQuery, debouncedColor]);

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
          </div>

          {setsLoading ? (
            <Loader message="Chargement des sets…" />
          ) : sets.length === 0 ? (
            <p className="py-12 text-center text-gray-500">Aucun set trouvé.</p>
          ) : (
            <>
              <p className="mb-3 text-sm text-gray-500">{sets.length} set(s)</p>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {sets.map((set) => (
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
                <option key={c.id} value={c.id === 1 ? '' : c.id}>
                  {c.name}
                </option>
              ))}
            </Select>
          </div>

          {partsLoading ? (
            <Loader message="Chargement des pièces…" />
          ) : parts.length === 0 ? (
            <p className="py-12 text-center text-gray-500">
              {partQuery ? 'Aucune pièce trouvée.' : 'Entrez un terme de recherche.'}
            </p>
          ) : (
            <>
              <p className="mb-3 text-sm text-gray-500">{parts.length} pièce(s)</p>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {parts.map((part) => (
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
