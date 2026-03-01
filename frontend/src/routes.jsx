import { createBrowserRouter } from 'react-router';
import RootLayout from './pages/RootLayout';
import HomePage from './pages/HomePage';
import SearchPage from './pages/SearchPage';
import AccountPage from './pages/AccountPage';
import LoginPage from './pages/LoginPage';
import NotFoundPage from './pages/NotFoundPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'search', element: <SearchPage /> },
      { path: 'account', element: <AccountPage /> },
      { path: 'login', element: <LoginPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
]);

export default router;
