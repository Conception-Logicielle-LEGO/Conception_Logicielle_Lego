// Données mock pour les pièces (pas d'endpoint backend)
export const mockParts = [
  { part_num: '3001', name: 'Brick 2x4', color: 'Red', quantity: 42, img_url: null },
  { part_num: '3002', name: 'Brick 2x3', color: 'Blue', quantity: 28, img_url: null },
  { part_num: '3003', name: 'Brick 2x2', color: 'Yellow', quantity: 56, img_url: null },
  { part_num: '3004', name: 'Brick 1x2', color: 'White', quantity: 120, img_url: null },
  { part_num: '3005', name: 'Brick 1x1', color: 'Black', quantity: 200, img_url: null },
  { part_num: '3020', name: 'Plate 2x4', color: 'Green', quantity: 15, img_url: null },
  { part_num: '3021', name: 'Plate 2x3', color: 'Red', quantity: 22, img_url: null },
  { part_num: '3022', name: 'Plate 2x2', color: 'Blue', quantity: 35, img_url: null },
  { part_num: '3023', name: 'Plate 1x2', color: 'Yellow', quantity: 80, img_url: null },
  { part_num: '3024', name: 'Plate 1x1', color: 'White', quantity: 150, img_url: null },
  { part_num: '3040', name: 'Roof Tile 1x2/45°', color: 'Dark Grey', quantity: 18, img_url: null },
  { part_num: '3660', name: 'Roof Tile 1x2 Inv', color: 'Light Grey', quantity: 12, img_url: null },
];

// Thèmes pour les filtres de recherche
export const themes = [
  { id: 1, name: 'Tous les thèmes' },
  { id: 2, name: 'City' },
  { id: 3, name: 'Technic' },
  { id: 4, name: 'Star Wars' },
  { id: 5, name: 'Harry Potter' },
  { id: 6, name: 'Creator' },
  { id: 7, name: 'Architecture' },
  { id: 8, name: 'Ideas' },
];

// Couleurs pour les filtres de pièces
export const colors = [
  { id: 1, name: 'Toutes les couleurs' },
  { id: 2, name: 'Red' },
  { id: 3, name: 'Blue' },
  { id: 4, name: 'Yellow' },
  { id: 5, name: 'Green' },
  { id: 6, name: 'White' },
  { id: 7, name: 'Black' },
  { id: 8, name: 'Light Grey' },
  { id: 9, name: 'Dark Grey' },
];
