import Container from 'react-bootstrap/Container';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from 'react-router-dom';
import ApiProvider from './contexts/ApiProvider';
import FlashProvider from './contexts/FlashProvider';
import Header from './components/Header';
import FeedPage from './pages/FeedPage';
import ExplorePage from './pages/ExplorePage';
import LikedPage from './pages/LikedPage';
import PrompterPage from './pages/PrompterPage';
import StoryPage from './pages/StoryPage';
import LoginPage from './pages/LoginPage';
import RegistrationPage from './pages/RegistrationPage';

function App() {
  return (
    <Container fluid className="App">
      <BrowserRouter>
        <FlashProvider>
          <ApiProvider>
            <Header />
            <Routes>
              <Route path="/" element={<FeedPage />} />
              <Route path="/explore" element={<ExplorePage />} />
              <Route path="/liked" element={<LikedPage />} />
              <Route path="/prompter/:id" element={<PrompterPage />} />
              <Route path="/story/:id" element={<StoryPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegistrationPage />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </ApiProvider>
        </FlashProvider>
      </BrowserRouter>
    </Container>
  );
}

export default App;
