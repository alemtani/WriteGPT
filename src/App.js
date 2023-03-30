import Container from 'react-bootstrap/Container';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from 'react-router-dom';
import ApiProvider from './contexts/ApiProvider';
import FlashProvider from './contexts/FlashProvider';
import UserProvider from './contexts/UserProvider';
import Header from './components/Header';
import FeedPage from './pages/FeedPage';
import ExplorePage from './pages/ExplorePage';
import LikedPage from './pages/LikedPage';
import PrompterPage from './pages/PrompterPage';
import StoryPage from './pages/StoryPage';
import LoginPage from './pages/LoginPage';
import RegistrationPage from './pages/RegistrationPage';
import EditPrompterPage from './pages/EditPrompterPage';
import EditStoryPage from './pages/EditStoryPage';
import ChangePasswordPage from './pages/ChangePasswordPage';
import PublicRoute from './components/PublicRoute';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <Container fluid className="App">
      <BrowserRouter>
        <FlashProvider>
          <ApiProvider>
            <UserProvider>
              <Header />
              <Routes>
                <Route path="/login" element={
                  <PublicRoute><LoginPage /></PublicRoute>
                } />
                <Route path="/register" element={
                  <PublicRoute><RegistrationPage /></PublicRoute>
                } />
                <Route path="*" element={
                  <PrivateRoute>
                    <Routes>
                      <Route path="/" element={<FeedPage />} />
                      <Route path="/explore" element={<ExplorePage />} />
                      <Route path="/liked" element={<LikedPage />} />
                      <Route path="/edit" element={<EditPrompterPage />} />
                      <Route path="/prompter/:id" element={<PrompterPage />} />
                      <Route path="/story/:id/edit" element={<EditStoryPage />} />
                      <Route path="/story/:id" element={<StoryPage />} />
                      <Route path="/password" element={<ChangePasswordPage />} />
                      <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                  </PrivateRoute>
                } />
              </Routes>
            </UserProvider>
          </ApiProvider>
        </FlashProvider>
      </BrowserRouter>
    </Container>
  );
}

export default App;
