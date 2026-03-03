import { createBrowserRouter } from 'react-router';
import RootLayout from './pages/RootLayout';
import HomePage from './pages/HomePage';
import SearchPage from './pages/SearchPage';
import AccountPage from './pages/AccountPage';
import BuildablePage from './pages/BuildablePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import NotFoundPage from './pages/NotFoundPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'search', element: <SearchPage /> },
      { path: 'buildable', element: <BuildablePage /> },
      { path: 'account', element: <AccountPage /> },
      { path: 'login', element: <LoginPage /> },
      { path: 'register', element: <RegisterPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
]);

export default router;
